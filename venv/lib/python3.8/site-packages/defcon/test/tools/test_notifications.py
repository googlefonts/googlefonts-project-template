import unittest
from defcon.tools.notifications import NotificationCenter
from defcon.test.testTools import NotificationTestObserver


class _TestObservable(object):

    def __init__(self, center, name):
        self.center = center
        self.name = name

    def __repr__(self):
        return "<_TestObservable {name} {id}".format(name=self.name, id=id(self))

    def postNotification(self, name):
        self.center.postNotification(name, self)


class NotificationCenterTest(unittest.TestCase):

    def __init__(self, methodName):
        unittest.TestCase.__init__(self, methodName)

    def test_addObserver_notification_observable(self):
        center = NotificationCenter()
        observable = _TestObservable(center, "Observable")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", observable)
        self.assertTrue(center.hasObserver(observer, "A", observable))
        self.assertFalse(center.hasObserver(observer, "B", observable))

    def test_addObserver_notification_no_observable(self):
        center = NotificationCenter()
        observable = _TestObservable(center, "Observable")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", None)
        self.assertTrue(center.hasObserver(observer, "A", None))
        self.assertFalse(center.hasObserver(observer, "A", observable))

    def test_addObserver_no_notification_observable(self):
        center = NotificationCenter()
        observable = _TestObservable(center, "Observable")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", None, observable)
        self.assertTrue(center.hasObserver(observer, None, observable))
        self.assertFalse(center.hasObserver(observer, "A", observable))

    def test_addObserver_no_notification_no_observable(self):
        center = NotificationCenter()
        observable = _TestObservable(center, "Observable")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", None, None)
        self.assertTrue(center.hasObserver(observer, None, None))
        self.assertFalse(center.hasObserver(observer, "A", observable))
        self.assertFalse(center.hasObserver(observer, None, observable))
        self.assertFalse(center.hasObserver(observer, "A", None))

    def test_removeObserver(self):
        center = NotificationCenter()
        observable = _TestObservable(center, "Observable")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", observable)
        center.removeObserver(observer, "A", observable)
        self.assertFalse(center.hasObserver(observer, "A", observable))

    def test_removeObserver_notification_observable(self):
        center = NotificationCenter()
        observable = _TestObservable(center, "Observable")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", observable)
        center.removeObserver(observer, "A", observable)
        self.assertFalse(center.hasObserver(observer, "A", observable))

    def test_removeObserver_allNotifications(self):
        center = NotificationCenter()
        observable1 = _TestObservable(center, "Observable1")
        observable2 = _TestObservable(center, "Observable2")
        observer1 = NotificationTestObserver()
        observer2 = NotificationTestObserver()
        center.addObserver(observer1, "notificationCallback", "A", observable1)
        center.addObserver(observer1, "notificationCallback", "B", observable1)
        center.addObserver(observer2, "notificationCallback", "A", observable1)
        center.addObserver(observer2, "notificationCallback", "B", observable1)
        center.addObserver(observer1, "notificationCallback", "A", observable2)
        center.addObserver(observer1, "notificationCallback", "B", observable2)
        center.addObserver(observer2, "notificationCallback", "A", observable2)
        center.addObserver(observer2, "notificationCallback", "B", observable2)
        center.removeObserver(observer1, "all", observable1)
        self.assertFalse(center.hasObserver(observer1, "A", observable1))
        self.assertFalse(center.hasObserver(observer1, "B", observable1))
        self.assertTrue(center.hasObserver(observer1, "A", observable2))
        self.assertTrue(center.hasObserver(observer1, "B", observable2))
        self.assertTrue(center.hasObserver(observer2, "A", observable1))
        self.assertTrue(center.hasObserver(observer2, "B", observable1))
        self.assertTrue(center.hasObserver(observer2, "A", observable2))
        self.assertTrue(center.hasObserver(observer2, "B", observable2))

    def test_removeObserver_notification_no_observable(self):
        center = NotificationCenter()
        _TestObservable(center, "Observable")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", None)
        center.removeObserver(observer, "A", None)
        self.assertFalse(center.hasObserver(observer, "A", None))

    def test_removeObserver_no_notification_observable(self):
        center = NotificationCenter()
        observable = _TestObservable(center, "Observable")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", None, observable)
        center.addObserver(observer, "notificationCallback", "A", observable)
        center.removeObserver(observer, None, observable)
        self.assertFalse(center.hasObserver(observer, None, observable))
        self.assertTrue(center.hasObserver(observer, "A", observable))

    def test_removeObserver_no_notification_no_observable(self):
        center = NotificationCenter()
        _TestObservable(center, "Observable")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", None, None)
        center.removeObserver(observer, None, None)
        self.assertFalse(center.hasObserver(observer, None, None))

    def test_postNotification_notification_observable(self):
        # notification, observable
        center = NotificationCenter()
        observable1 = _TestObservable(center, "Observable1")
        observable2 = _TestObservable(center, "Observable2")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", observable1)
        center.postNotification("A", observable1)
        self.assertEqual(observer.stack[-1], ("A", "Observable1"))
        center.postNotification("A", observable2)
        self.assertEqual(observer.stack[-1], ("A", "Observable1"))
        center.postNotification("B", observable1)
        self.assertEqual(observer.stack[-1], ("A", "Observable1"))
        center.postNotification("B", observable2)
        self.assertEqual(observer.stack[-1], ("A", "Observable1"))

    def test_postNotification_notification_no_observable(self):
        # notification, no observable
        center = NotificationCenter()
        observable1 = _TestObservable(center, "Observable1")
        observable2 = _TestObservable(center, "Observable2")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", None)
        center.postNotification("A", observable1)
        self.assertEqual(observer.stack[-1], ("A", "Observable1"))
        center.postNotification("A", observable2)
        self.assertEqual(observer.stack[-1], ("A", "Observable2"))
        center.postNotification("B", observable1)
        self.assertEqual(observer.stack[-1], ("A", "Observable2"))
        center.postNotification("B", observable2)
        self.assertEqual(observer.stack[-1], ("A", "Observable2"))

    def test_postNotification_no_notification_observable(self):
        # no notification, observable
        center = NotificationCenter()
        observable1 = _TestObservable(center, "Observable1")
        observable2 = _TestObservable(center, "Observable2")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", None, observable1)
        center.postNotification("A", observable1)
        self.assertEqual(observer.stack[-1], ("A", "Observable1"))
        center.postNotification("A", observable2)
        center.postNotification("B", observable1)
        self.assertEqual(observer.stack[-1], ("B", "Observable1"))
        center.postNotification("B", observable2)

    def test_postNotification_no_notification_no_observable(self):
        # no notification, no observable
        center = NotificationCenter()
        observable1 = _TestObservable(center, "Observable1")
        observable2 = _TestObservable(center, "Observable2")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", None, None)
        center.postNotification("A", observable1)
        self.assertEqual(observer.stack[-1], ("A", "Observable1"))
        center.postNotification("A", observable2)
        self.assertEqual(observer.stack[-1], ("A", "Observable2"))
        center.postNotification("B", observable1)
        self.assertEqual(observer.stack[-1], ("B", "Observable1"))
        center.postNotification("B", observable2)
        self.assertEqual(observer.stack[-1], ("B", "Observable2"))

    def test_hold_and_releaseHeldNotifications_all_notifications(self):
        "Hold all notifications"
        center = NotificationCenter()
        observable1 = _TestObservable(center, "Observable1")
        observable2 = _TestObservable(center, "Observable2")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", observable1)
        center.addObserver(observer, "notificationCallback", "B", observable1)
        center.addObserver(observer, "notificationCallback", "C", observable2)
        center.holdNotifications()
        observable1.postNotification("A")
        self.assertEqual(len(observer.stack), 0)
        observable1.postNotification("A")
        self.assertEqual(len(observer.stack), 0)
        observable1.postNotification("B")
        self.assertEqual(len(observer.stack), 0)
        observable2.postNotification("C")
        self.assertEqual(len(observer.stack), 0)
        center.releaseHeldNotifications()
        self.assertEqual(observer.stack[-3], ("A", "Observable1"))
        self.assertEqual(observer.stack[-2], ("B", "Observable1"))
        self.assertEqual(observer.stack[-1], ("C", "Observable2"))
        self.assertEqual(len(observer.stack), 3)

    def test_hold_and_releaseHeldNotifications_notifications_of_observable(self):
        "Hold all notifications of a specific observable"
        center = NotificationCenter()
        observable1 = _TestObservable(center, "Observable1")
        observable2 = _TestObservable(center, "Observable2")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", observable1)
        center.addObserver(observer, "notificationCallback", "B", observable1)
        center.addObserver(observer, "notificationCallback", "C", observable2)
        center.holdNotifications(observable=observable1)
        observable1.postNotification("A")
        observable1.postNotification("A")
        observable1.postNotification("B")
        observable2.postNotification("C")
        self.assertEqual(observer.stack[-1], ("C", "Observable2"))
        center.releaseHeldNotifications(observable=observable1)
        self.assertEqual(observer.stack[-2], ("A", "Observable1"))
        self.assertEqual(observer.stack[-1], ("B", "Observable1"))
        self.assertEqual(len(observer.stack), 3)

    def test_hold_and_releaseHeldNotifications_notifications_of_observable(
            self):
        "Hold all notifications of a specific notification"
        center = NotificationCenter()
        observable1 = _TestObservable(center, "Observable1")
        observable2 = _TestObservable(center, "Observable2")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", observable1)
        center.addObserver(observer, "notificationCallback", "B", observable1)
        center.addObserver(observer, "notificationCallback", "C", observable2)
        center.holdNotifications(notification="A")
        observable1.postNotification("A")
        observable1.postNotification("A")
        observable1.postNotification("B")
        self.assertEqual(observer.stack[-1], ("B", "Observable1"))
        observable2.postNotification("C")
        self.assertEqual(observer.stack[-1], ("C", "Observable2"))
        center.releaseHeldNotifications(notification="A")
        self.assertEqual(observer.stack[-1], ("A", "Observable1"))
        self.assertEqual(len(observer.stack), 3)

    def test_areNotificationsHeld_all_held(self):
        center = NotificationCenter()
        observable = _TestObservable(center, "Observable")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", observable)
        center.holdNotifications()
        self.assertTrue(center.areNotificationsHeld())
        center.releaseHeldNotifications()
        self.assertFalse(center.areNotificationsHeld())

    def test_areNotificationsHeld_observable_off(self):
        center = NotificationCenter()
        observable1 = _TestObservable(center, "Observable1")
        observable2 = _TestObservable(center, "Observable2")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", observable1)
        center.addObserver(observer, "notificationCallback", "B", observable2)
        center.holdNotifications(observable=observable1)
        self.assertTrue(center.areNotificationsHeld(observable=observable1))
        self.assertFalse(center.areNotificationsHeld(observable=observable2))
        center.releaseHeldNotifications(observable=observable1)
        self.assertFalse(center.areNotificationsHeld(observable=observable1))

    def test_areNotificationsHeld_notification_off(self):
        center = NotificationCenter()
        observable = _TestObservable(center, "Observable")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", observable)
        center.addObserver(observer, "notificationCallback", "B", observable)
        center.holdNotifications(notification="A")
        self.assertTrue(center.areNotificationsHeld(notification="A"))
        self.assertFalse(center.areNotificationsHeld(notification="B"))
        center.releaseHeldNotifications(notification="A")
        self.assertFalse(center.areNotificationsHeld(notification="A"))

    def test_areNotificationsHeld_observer_off(self):
        center = NotificationCenter()
        observable = _TestObservable(center, "Observable")
        observer1 = NotificationTestObserver()
        observer2 = NotificationTestObserver()
        center.addObserver(observer1, "notificationCallback", "A", observable)
        center.addObserver(observer2, "notificationCallback", "A", observable)
        center.holdNotifications(observer=observer1)
        self.assertTrue(center.areNotificationsHeld(observer=observer1))
        self.assertFalse(center.areNotificationsHeld(observer=observer2))
        center.releaseHeldNotifications(observer=observer1)
        self.assertFalse(center.areNotificationsHeld(observer=observer1))

    def test_disable_enableNotifications_all_notifications(self):
        # disable all notifications
        center = NotificationCenter()
        observable1 = _TestObservable(center, "Observable1")
        observable2 = _TestObservable(center, "Observable2")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", observable1)
        center.addObserver(observer, "notificationCallback", "B", observable1)
        center.addObserver(observer, "notificationCallback", "C", observable2)
        center.disableNotifications()
        observable1.postNotification("A")
        observable1.postNotification("B")
        observable2.postNotification("C")
        center.enableNotifications()
        observable1.postNotification("A")
        self.assertEqual(observer.stack[-1], ("A", "Observable1"))

    def test_disable_enableNotifications_specific_observable(self):
        # disable all notifications for a specific observable
        center = NotificationCenter()
        observable1 = _TestObservable(center, "Observable1")
        observable2 = _TestObservable(center, "Observable2")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", observable1)
        center.addObserver(observer, "notificationCallback", "B", observable1)
        center.addObserver(observer, "notificationCallback", "C", observable2)
        center.disableNotifications(observable=observable1)
        observable1.postNotification("A")
        observable1.postNotification("B")
        observable2.postNotification("C")
        self.assertEqual(observer.stack[-1], ("C", "Observable2"))
        center.enableNotifications(observable=observable1)
        observable1.postNotification("A")
        self.assertEqual(observer.stack[-1], ("A", "Observable1"))

    def test_disable_enableNotifications_specific_notification(self):
        # disable all notifications for a specific notification
        center = NotificationCenter()
        observable1 = _TestObservable(center, "Observable1")
        observable2 = _TestObservable(center, "Observable2")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", observable1)
        center.addObserver(observer, "notificationCallback", "B", observable1)
        center.addObserver(observer, "notificationCallback", "C", observable2)
        center.disableNotifications(notification="A")
        observable1.postNotification("A")
        observable1.postNotification("B")
        self.assertEqual(observer.stack[-1], ("B", "Observable1"))
        observable2.postNotification("C")
        self.assertEqual(observer.stack[-1], ("C", "Observable2"))
        center.enableNotifications(notification="A")
        observable1.postNotification("A")
        self.assertEqual(observer.stack[-1], ("A", "Observable1"))

    def test_disable_enableNotifications_specific_observer(self):
        # disable all notifications for a specific observer
        center = NotificationCenter()
        observable1 = _TestObservable(center, "Observable1")
        observable2 = _TestObservable(center, "Observable2")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", observable1)
        center.addObserver(observer, "notificationCallback", "B", observable1)
        center.addObserver(observer, "notificationCallback", "C", observable2)
        center.disableNotifications(observer=observer)
        observable1.postNotification("A")
        observable1.postNotification("B")
        observable2.postNotification("C")
        center.enableNotifications(observer=observer)
        observable1.postNotification("A")
        self.assertEqual(observer.stack[-1], ("A", "Observable1"))

    def test_areNotificationsDisabled_all_off(self):
        center = NotificationCenter()
        observable1 = _TestObservable(center, "Observable1")
        observable2 = _TestObservable(center, "Observable2")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", observable1)
        center.addObserver(observer, "notificationCallback", "B", observable2)
        center.disableNotifications()
        self.assertTrue(center.areNotificationsDisabled())
        center.enableNotifications()
        self.assertFalse(center.areNotificationsDisabled())

    def test_areNotificationsDisabled_observable_off(self):
        center = NotificationCenter()
        observable1 = _TestObservable(center, "Observable1")
        observable2 = _TestObservable(center, "Observable2")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", observable1)
        center.addObserver(observer, "notificationCallback", "B", observable2)
        center.disableNotifications(observable=observable1)
        self.assertTrue(
            center.areNotificationsDisabled(observable=observable1))
        self.assertFalse(
            center.areNotificationsDisabled(observable=observable2))
        center.enableNotifications(observable=observable1)
        self.assertFalse(
            center.areNotificationsDisabled(observable=observable1))

    def test_areNotificationsDisabled_notification_off(self):
        center = NotificationCenter()
        observable1 = _TestObservable(center, "Observable1")
        observable2 = _TestObservable(center, "Observable2")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", observable1)
        center.addObserver(observer, "notificationCallback", "B", observable2)
        center.disableNotifications(notification="A")
        self.assertTrue(center.areNotificationsDisabled(notification="A"))
        self.assertFalse(center.areNotificationsDisabled(notification="B"))
        center.enableNotifications(notification="A")
        self.assertFalse(center.areNotificationsDisabled(notification="A"))

    def test_areNotificationsDisabled_observer_off(self):
        center = NotificationCenter()
        observable1 = _TestObservable(center, "Observable1")
        observer1 = NotificationTestObserver()
        observer2 = NotificationTestObserver()
        center.addObserver(observer1, "notificationCallback", "A", observable1)
        center.addObserver(observer2, "notificationCallback", "A", observable1)
        center.disableNotifications(observer=observer1)
        self.assertTrue(center.areNotificationsDisabled(observer=observer1))
        self.assertFalse(center.areNotificationsDisabled(observer=observer2))
        center.enableNotifications(observer=observer1)
        self.assertFalse(center.areNotificationsDisabled(observer=observer1))

    def test_addObserver_identifier(self):
        center = NotificationCenter()
        observable = _TestObservable(center, "Observable")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", observable, identifier="identifier1")
        center.addObserver(observer, "notificationCallback", "B", observable, identifier="identifier2")
        expected = [
            dict(observer=observer, observable=observable, notification="A", identifier="identifier1"),
            dict(observer=observer, observable=observable, notification="B", identifier="identifier2")
        ]
        result = center.findObservations()
        self.assertEqual(result, expected)

    def test_addObserver_identifierDuplicate(self):
        center = NotificationCenter()
        observable = _TestObservable(center, "Observable")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", observable, identifier="identifier1")
        center.addObserver(observer, "notificationCallback", "B", observable, identifier="identifier1")
        expected = [
            dict(observer=observer, observable=observable, notification="A", identifier="identifier1"),
            dict(observer=observer, observable=observable, notification="B", identifier="identifier1")
        ]
        self.assertEqual(center.findObservations(), expected)

    def test_removeObserver_identifier(self):
        center = NotificationCenter()
        observable = _TestObservable(center, "Observable")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", observable, identifier="identifier1")
        center.addObserver(observer, "notificationCallback", "B", observable, identifier="identifier2")
        center.removeObserver(observer, "A", observable)
        center.removeObserver(observer, "B", observable)
        expected = []
        self.assertEqual(center.findObservations(), expected)

    def _buildFindObservationsObjects(self):
        center = NotificationCenter()
        observable1 = _TestObservable(center, "Observable1")
        observable2 = _TestObservable(center, "Observable2")
        observer1 = NotificationTestObserver(name="Observer1")
        observer2 = NotificationTestObserver(name="Observer2")
        center.addObserver(observer1, "notificationCallback", "A", observable1, identifier="identifier1-1-A")
        center.addObserver(observer1, "notificationCallback", "B", observable1, identifier="identifier1-1-B")
        center.addObserver(observer1, "notificationCallback", "A", observable2, identifier="identifier1-2-A")
        center.addObserver(observer1, "notificationCallback", "B", observable2, identifier="identifier1-2-B")
        center.addObserver(observer2, "notificationCallback", "A", observable1, identifier="identifier2-1-A")
        center.addObserver(observer2, "notificationCallback", "B", observable1, identifier="identifier2-1-B")
        center.addObserver(observer2, "notificationCallback", "A", observable2, identifier="identifier2-2-A")
        center.addObserver(observer2, "notificationCallback", "B", observable2, identifier="identifier2-2-B")
        return center, observer1, observer2, observable1, observable2

    def test_findObservations_observer(self):
        center, observer1, observer2, observable1, observable2 = self._buildFindObservationsObjects()
        expected = [
            dict(observer=observer1, notification="A", observable=observable1, identifier="identifier1-1-A"),
            dict(observer=observer1, notification="B", observable=observable1, identifier="identifier1-1-B"),
            dict(observer=observer1, notification="A", observable=observable2, identifier="identifier1-2-A"),
            dict(observer=observer1, notification="B", observable=observable2, identifier="identifier1-2-B")
        ]
        result = center.findObservations(observer=observer1)
        self.assertEqual(result, expected)

    def test_findObservations_observable(self):
        center, observer1, observer2, observable1, observable2 = self._buildFindObservationsObjects()
        expected = [
            dict(observer=observer1, notification="A", observable=observable1, identifier="identifier1-1-A"),
            dict(observer=observer2, notification="A", observable=observable1, identifier="identifier2-1-A"),
            dict(observer=observer1, notification="B", observable=observable1, identifier="identifier1-1-B"),
            dict(observer=observer2, notification="B", observable=observable1, identifier="identifier2-1-B")
        ]
        result = center.findObservations(observable=observable1)
        self.assertEqual(result, expected)

    def test_findObservations_notification(self):
        center, observer1, observer2, observable1, observable2 = self._buildFindObservationsObjects()
        expected = [
            dict(observer=observer1, notification="A", observable=observable1, identifier="identifier1-1-A"),
            dict(observer=observer2, notification="A", observable=observable1, identifier="identifier2-1-A"),
            dict(observer=observer1, notification="A", observable=observable2, identifier="identifier1-2-A"),
            dict(observer=observer2, notification="A", observable=observable2, identifier="identifier2-2-A")
        ]
        result = center.findObservations(notification="A")
        self.assertEqual(result, expected)

    def test_findObservations_identifier(self):
        center, observer1, observer2, observable1, observable2 = self._buildFindObservationsObjects()
        expected = [
            dict(observer=observer1, notification="A", observable=observable1, identifier="identifier1-1-A")
        ]
        result = center.findObservations(identifier="identifier1-1-A")
        self.assertEqual(result, expected)

    def test_findObservations_identifierPattern(self):
        center, observer1, observer2, observable1, observable2 = self._buildFindObservationsObjects()
        expected = [
            dict(observer=observer1, notification="A", observable=observable1, identifier="identifier1-1-A"),
            dict(observer=observer1, notification="A", observable=observable2, identifier="identifier1-2-A")
        ]
        result = center.findObservations(identifier="identifier1-*-A")
        self.assertEqual(result, expected)

    def test_findObservations_all(self):
        center, observer1, observer2, observable1, observable2 = self._buildFindObservationsObjects()
        expected = [
            dict(observer=observer1, notification="A", observable=observable1, identifier="identifier1-1-A")
        ]
        result = center.findObservations(observer=observer1, notification="A", observable=observable1, identifier="identifier1-1-A")
        self.assertEqual(result, expected)

    def test_findObservations_noIdentifier(self):
        center = NotificationCenter()
        observable = _TestObservable(center, "Observable")
        observer = NotificationTestObserver()
        center.addObserver(observer, "notificationCallback", "A", observable, identifier="identifier1")
        center.addObserver(observer, "notificationCallback", "B", observable)
        expected = [
            dict(observer=observer, observable=observable, notification="A", identifier="identifier1"),
            dict(observer=observer, observable=observable, notification="B", identifier=None)
        ]
        result = center.findObservations()
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
