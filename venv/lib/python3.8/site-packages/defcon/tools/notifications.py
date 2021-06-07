"""
A flexible and relatively robust implementation
of the Observer Pattern.
"""

from __future__ import print_function
from collections import OrderedDict
import sys
import weakref
from fnmatch import fnmatchcase

"""

----------------------
Internal Documentation
----------------------

Storage Structures:

registry : {
        (notification, observable) : OrderedDict(
            observer : method name
        )
}

holds : {
    (notification, observable, observer) : {
        count=int,
        notifications=[
            (notification name, observable ref, data)
        ]
    )
}

disabled : {
    (notification, observable, observer) : count
}

identifierRegistry : {
        (notification, observable) : OrderedDict(
            observer : identifier
        )
}

"""


class NotificationCenter(object):

    def __init__(self):
        self._registry = {}
        self._observerKeyBacktrack = {}
        self._holds = {}
        self._disabled = {}
        self._identifierRegistry = {}

    # -----
    # Basic
    # -----

    def addObserver(self, observer, methodName, notification=None, observable=None, identifier=None):
        """
        Add an observer to this notification dispatcher.

        * **observer** An object that can be referenced with weakref.
        * **methodName** A string representing the method to be called
          when the notification is posted.
        * **notification** The notification that the observer should
          be notified of. If this is None, all notifications for
          the *observable* will be posted to *observer*.
        * **observable** The object to observe. If this is None,
          all notifications with the name provided as *notification*
          will be posted to the *observer*.
        * **identifier** None or a string identifying the observation.
          There is no requirement that the string be unique. A reverse
          domain naming scheme is recommended, but there are no
          requirements for the structure of the string.

        If None is given for both *notification* and *observable*
        **all** notifications posted will be sent to the given method
        of the observer.

        The method that will be called as a result of the action
        must accept a single *notification* argument. This will
        be a :class:`Notification` object.
        """
        assert notification != "all", "'all' is a reserved name and can not be used as a notification."
        if observable is not None:
            observable = weakref.ref(observable)
        observer = weakref.ref(observer)
        key = (notification, observable)
        if key not in self._registry:
            self._registry[key] = OrderedDict()
        assert observer not in self._registry[key],\
            "An observer is only allowed to have one callback for a given notification + observable combination. notification={notification}, observable={observable} , observer={observer}, existing method={method1}, adding method={method2}".format(
                notification=key[0], observable=key[1](), observer=observer(), method1=self._registry[key][observer], method2=methodName
            )
        self._registry[key][observer] = methodName
        if observer not in self._observerKeyBacktrack:
            self._observerKeyBacktrack[observer] = {}
        if observable not in self._observerKeyBacktrack[observer]:
            self._observerKeyBacktrack[observer][observable] = set()
        self._observerKeyBacktrack[observer][observable].add(key)
        if identifier is not None:
            if key not in self._identifierRegistry:
                self._identifierRegistry[key] = OrderedDict()
            self._identifierRegistry[key][observer] = identifier

    def hasObserver(self, observer, notification, observable):
        """
        Returns a boolean indicating if the **observer** is registered
        for **notification** posted by **observable**. Either
        *observable* or *notification* may be None.
        """
        if observable is not None:
            observable = weakref.ref(observable)
        key = (notification, observable)
        if key not in self._registry:
            return False
        observer = weakref.ref(observer)
        return observer in self._registry[key]

    def removeObserver(self, observer, notification, observable=None):
        """
        Remove an observer from this notification dispatcher.

        * **observer** A registered object.
        * **notification** The notification that the observer was registered
          to be notified of. If this is `"all"`, all notifications for
          the *observable* will be removed for *observer*.
        * **observable** The object being observed.
        """
        if observable is not None:
            observable = weakref.ref(observable)
        observer = weakref.ref(observer)
        if notification == "all":
            keys = set(self._observerKeyBacktrack[observer][observable])
        else:
            keys = [
                (notification, observable)
            ]
        for key in keys:
            if key not in self._registry:
                continue
            if observer in self._registry[key]:
                del self._registry[key][observer]
            if not len(self._registry[key]):
                del self._registry[key]
            if observer in self._observerKeyBacktrack:
                if observable in self._observerKeyBacktrack[observer]:
                    if key in self._observerKeyBacktrack[observer][observable]:
                        self._observerKeyBacktrack[observer][observable].remove(key)
                    if not self._observerKeyBacktrack[observer][observable]:
                        del self._observerKeyBacktrack[observer][observable]
                if not self._observerKeyBacktrack[observer]:
                    del self._observerKeyBacktrack[observer]
            if key in self._identifierRegistry:
                if observer in self._identifierRegistry[key]:
                    del self._identifierRegistry[key][observer]
                if not len(self._identifierRegistry[key]):
                    del self._identifierRegistry[key]

    def postNotification(self, notification, observable, data=None):
        assert notification is not None
        assert observable is not None
        observableRef = weakref.ref(observable)
        # observer independent hold/disabled
        # ----------------------------------
        if self._holds or self._disabled:
            holdDisabledPossibilities = (
                # least specific -> most specific
                # suspended for all
                (None, None, None),
                # suspended for this notification
                (notification, None, None),
                # suspended for this observer
                (None, observableRef, None),
                # suspended for this notification + observable
                (notification, observableRef, None)
            )
            for key in holdDisabledPossibilities:
                if key in self._disabled:
                    return
                if key in self._holds:
                    n = (notification, observableRef, data)
                    if n not in self._holds[key]["notifications"]:
                        self._holds[key]["notifications"].append(n)
                    return
        # posting
        # -------
        notificationObj = Notification(notification, observableRef, data)
        registryPossibilities = (
            # least specific -> most specific
            (None, None),
            (None, observableRef),
            (notification, None),
            (notification, observableRef),
        )
        for key in registryPossibilities:
            if key not in self._registry:
                continue
            for observerRef, methodName in list(self._registry[key].items()):
                # observer specific hold/disabled
                # -------------------------------
                if self._holds or self._disabled:
                    holdDisabledPossibilities = (
                        # least specific -> most specific
                        # suspended for observer
                        (None, None, observerRef),
                        # suspended for notification + observer
                        (notification, None, observerRef),
                        # suspended for observable + observer
                        (None, observableRef, observerRef),
                        # suspended for notification + observable + observer
                        (notification, observableRef, observerRef)
                    )
                    disabled = False
                    if self._disabled:
                        for disableKey in holdDisabledPossibilities:
                            if disableKey in self._disabled:
                                disabled = True
                                break
                    if disabled:
                        continue
                    hold = False
                    if self._holds:
                        for holdKey in holdDisabledPossibilities:
                            if holdKey in self._holds:
                                hold = True
                                n = (notification, observableRef, data)
                                if n not in self._holds[key]["notifications"]:
                                    self._holds[holdKey]["notifications"].append(n)
                                break
                    if hold:
                        continue
                # post
                # ----
                observer = observerRef()
                if observer is None:
                    # dead ref.
                    # XXX: delete?
                    continue
                callback = getattr(observer, methodName)
                callback(notificationObj)

    # ----
    # Hold
    # ----

    def holdNotifications(self, observable=None, notification=None, observer=None, note=None):
        """
        Hold all notifications posted to all objects observing
        **notification** in **observable**.

        * **observable** The object that the notification belongs to. This is optional.
          If no *observable* is given, *all* *notifications* will be held.
        * **notification** The name of the notification. This is optional.
          If no *notification* is given, *all* notifications for *observable*
          will be held.
        * **observer** The specific observer to not hold notifications for.
          If no *observer* is given, the appropriate notifications will be
          held for all observers.
        * **note** An arbitrary string containing information about why the hold
          has been requested, the requester, etc. This is used for reference only.

        Held notifications will be posted after the matching *notification*
        and *observable* have been passed to :meth:`Notification.releaseHeldNotifications`.
        This object will retain a count of how many times it has been told to
        hold notifications for *notification* and *observable*. It will not
        post the notifications until the *notification* and *observable*
        have been released the same number of times.
        """
        if observable is not None:
            observable = weakref.ref(observable)
        if observer is not None:
            observer = weakref.ref(observer)
        key = (notification, observable, observer)
        if key not in self._holds:
            self._holds[key] = dict(count=0, notifications=[], notes=[])
        self._holds[key]["count"] += 1
        if note is not None:
            self._holds[key]["notes"].append(note)

    def releaseHeldNotifications(self, observable=None, notification=None, observer=None):
        """
        Release all held notifications posted to all objects observing
        **notification** in **observable**.

        * **observable** The object that the notification belongs to. This is optional.
        * **notification** The name of the notification. This is optional.
        * **observer** The observer. This is optional.
        """
        if observable is not None:
            observable = weakref.ref(observable)
        if observer is not None:
            observer = weakref.ref(observer)
        key = (notification, observable, observer)
        self._holds[key]["count"] -= 1
        if self._holds[key]["count"] == 0:
            notifications = self._holds[key]["notifications"]
            del self._holds[key]
            for notification, observableRef, data in notifications:
                self.postNotification(notification, observableRef(), data)

    def areNotificationsHeld(self, observable=None, notification=None, observer=None):
        """
        Returns a boolean indicating if notifications posted to all objects observing
        **notification** in **observable** are being held.

        * **observable** The object that the notification belongs to. This is optional.
        * **notification** The name of the notification. This is optional.
        * **observer** The observer. This is optional.
        """
        if observable is not None:
            observable = weakref.ref(observable)
        if observer is not None:
            observer = weakref.ref(observer)
        key = (notification, observable, observer)
        return key in self._holds

    def getHeldNotifications(self):
        """
        Returns a list of all held notifications. This will be a
        tuple of the form:

        (notification, observable, observer)
        """
        return self._holds.keys()

    def getHeldNotificationNotes(self, observable=None, notification=None, observer=None):
        """
        Returns a list of notes defined for notification holds observing
        **notification** in **observable** are being held.

        * **observable** The object that the notification belongs to. This is optional.
        * **notification** The name of the notification. This is optional.
        * **observer** The observer. This is optional.
        """
        if observable is not None:
            observable = weakref.ref(observable)
        if observer is not None:
            observer = weakref.ref(observer)
        key = (notification, observable, observer)
        return self._holds[key]["notes"]

    # -------
    # Disable
    # -------

    def disableNotifications(self, observable=None, notification=None, observer=None):
        """
        Disable all posts of **notification** from **observable** posted
        to **observer** observing.

        * **observable** The object that the notification belongs to. This is optional.
          If no *observable* is given, *all* *notifications* will be disabled for *observer*.
        * **notification** The name of the notification. This is optional.
          If no *notification* is given, *all* notifications for *observable*
          will be disabled for *observer*.
        * **observer** The specific observer to not send posts to. If no
          *observer* is given, the appropriate notifications will not
          be posted to any observers.

        This object will retain a count of how many times it has been told to
        disable notifications for *notification* and *observable*. It will not
        enable new notifications until the *notification* and *observable*
        have been released the same number of times.
        """
        if observable is not None:
            observable = weakref.ref(observable)
        if observer is not None:
            observer = weakref.ref(observer)
        key = (notification, observable, observer)
        if key not in self._disabled:
            self._disabled[key] = 0
        self._disabled[key] += 1

    def enableNotifications(self, observable=None, notification=None, observer=None):
        """
        Enable notifications posted to all objects observing
        **notification** in **observable**.

        * **observable** The object that the notification belongs to. This is optional.
        * **notification** The name of the notification. This is optional.
        * **observer** The observer. This is optional.
        """
        if observable is not None:
            observable = weakref.ref(observable)
        if observer is not None:
            observer = weakref.ref(observer)
        key = (notification, observable, observer)
        self._disabled[key] -= 1
        if self._disabled[key] == 0:
            del self._disabled[key]

    def areNotificationsDisabled(self, observable=None, notification=None, observer=None):
        """
        Returns a boolean indicating if notifications posted to all objects observing
        **notification** in **observable** are disabled.

        * **observable** The object that the notification belongs to. This is optional.
        * **notification** The name of the notification. This is optional.
        * **observer** The observer. This is optional.
        """
        if observable is not None:
            observable = weakref.ref(observable)
        if observer is not None:
            observer = weakref.ref(observer)
        key = (notification, observable, observer)
        return key in self._disabled

    # ----
    # Find
    # ----

    def findObservations(self, observer=None, notification=None, observable=None, identifier=None):
        """
        Find observations matching the given arguments based
        on the values that were passed during addObserver.
        A value of None for any of these indicates that all
        should be considered to match the value. In the case
        of identifier, strings will be matched using fnmatch.fnmatchcase.
        The returned value will be a list of dictionaries with
        this format:

            [
                {
                    observer=<...>
                    observable=<...>
                    methodName="..."
                    notification="..."
                    identifier="..."
                }
            ]
        """
        if observer is not None:
            observer = weakref.ref(observer)
        if observable is not None:
            observable = weakref.ref(observable)
        found = []
        for (otherNotification, otherObservable), observerDict in self._registry.items():
            if notification is not None:
                if otherNotification != notification:
                    continue
            if observable is not None:
                if otherObservable != observable:
                    continue
            for otherObserver, methodName in observerDict.items():
                otherIdentifier = None
                if (otherNotification, otherObservable) in self._identifierRegistry:
                    otherIdentifier = self._identifierRegistry[otherNotification, otherObservable].get(otherObserver)
                if otherIdentifier is None and identifier is not None:
                    continue
                if otherIdentifier is not None and identifier is not None:
                    if not fnmatchcase(otherIdentifier, identifier):
                        continue
                if observer is not None:
                    if otherObserver != observer:
                        continue
                observation = dict(
                    observer=otherObserver(),
                    observable=otherObservable(),
                    notification=otherNotification,
                    identifier=otherIdentifier
                )
                found.append(observation)
        return found


class Notification(object):

    """An object that wraps notification data."""

    __slots__ = ("_name", "_objRef", "_data")

    def __init__(self, name, objRef, data):
        self._name = name
        self._objRef = objRef
        self._data = data

    def __repr__(self):
        return "<Notification: %s %s>" % (self.name, repr(self.object))

    def _get_name(self):
        return self._name

    name = property(_get_name, doc="The notification name. A string.")

    def _get_object(self):
        if self._objRef is not None:
            return self._objRef()
        return None

    object = property(_get_object, doc="The observable object the notification belongs to.")

    def _get_data(self):
        return self._data

    data = property(_get_data, doc="Arbitrary data passed along with the notification. There is no set format for this data and there is not requirement that any data be present. Refer to the documentation for methods that are responsible for generating notifications for information about this data.")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
