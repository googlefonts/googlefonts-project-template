import unittest
import collections
from fontParts.base import FontPartsError

testPNGData = """
89504e470d0a1a0a0000000d4948445200000080000000800806000000c33e61cb0000
02ee694343504943432050726f66696c65000078018554cf6b134114fe366ea9d02208
5a6b0eb27890224959ab6845d436fd11626b0cdb1fb64590643349d66e36ebee26b5a5
88e4e2d12ade45eda107ff801e7af0642f4a855a4528deab2862a1172df1cd6e4cb6a5
eac0ce7ef3de37ef7d6f76df000d72d234f58004e40dc752a211696c7c426afc88008e
a20941342555dbec4e2406418373f97be7d87a0f815b56c37bfb77b277ad9ad2b69a07
84fd40e0479ad92ab0ef17710a591202883cdfa129c77408dfe3d8f2ec8f394e7978c1
b50f2b3dc459227c40352dce7f4db853cd25d34083483894f571523e9cd78b94d71d07
696e66c6c810bd4f90a6bbcceeab62a19c4ef60e90bd9df47e4eb3de3ec221c20b19ad
3f46b88d9ef58cd53fe261e1a4e6c4863d1c1835f4f86015b71aa9f835c2145f104d27
a25471d92e0df198aefd56f24a82709038ca646180735a484fd74c6ef8ba87057d26d7
13afe2775651e1798f1367ded4ddef45da02af300e1d0c1a0c9a0d48501045046198b0
5040863c1a3134b2723f23ab061b937b3275246abb746244b1417b36dc3db751a4dd3c
fe2822719443b50892fc41fe2aafc94fe579f9cb5cb0d856f794ad9b9abaf2e03bc5e5
99b91a1ed7d3c8e3734d5e7c95d47693574796ac797abc9aec1a3fec579731e682358f
c473b0fbf12d5f95cc97298c14c5e355f3ea4b84755a3137df9f6c7f3b3de22ecf2eb5
d673ad898b37569b9767fd6a48fbeeaabc93e655f94f5ef5f1fc67cdc463e229312676
8ae7218997c52ef192d84bab0be2606dc7089d958629d26d91fa24d560609abcf52f5d
3f5b78bd467f0cf5519419ccd25489f77fc22a64349db90e6ffa8fdbc7fc17e4f78ae7
9f28022f6ce0c899ba6d5371ef10a165a56e73ae0217bfd17df0b66e6ba37e38fc0458
3cab16ad52359f20bc011c76877a1ee82998d39696cd3952872c9f93bae9ca6252cc50
db435252d725d7654b16b3995562e976d899d31d6e1ca13942f7c4a74a6593faaff111
b0fdb052f9f9ac52d97e4e1ad68197fa6fc0bcfd45c0788b8900000009704859730000
0b1300000b1301009a9c1800001ea3494441547801ed9d578c1dc59ac77b926d8c0360
9c6dec019383c0cb72612f4164010ff000175878602584001184b80fc003d24a2b2178
4144ed5e5602b1c2c6d2458056225d0c0f5c049820e20513cc1a6430c9018fd3cc9c99
fd7e55e73fa74ebb4fe83e3d33a7614aaa53d515beaafabe7f7d15baba4e4794a3e9e8
e888bacc24901cb6b00e850f0ff3586dc85b2b9c94f138d22785139644ab5e7a4728f9
a7aade9664786868c8aa92d080e4fc6d1f3a22948c35557e5cf94b196915251b18ef36
20940c074356e910cda1bf10ede9cea1969dd6bbba8c19a579f3e61d76fbedb7ff47d0
43048aaa62d41b2d9078c7343a552c9c3c23a4ca71a2572b7c244f9c1619ccb8322c4e
74460a505c9940a8714cd643c33ffffcf386b7df7efbef6bd6acf9fbb66ddbbeefecec
dcab9c76c05c0161a43dc415c18c30224365c98b355e744e3626f51f71c41167bcfbee
bb2fc0b0725c5db2301d13c8c33d670d8fd3129d303c0c7385957faccece17c613265b
2a958677eddad5b16eddba0dcf3cf3cce38f3efae8fd0684cdd6f61e4bb3db320b0434
ca37ac4cbb9d9d3c00d06d4c98624c183af4d043cf58bd7af5b3e61db446b7427b4c79
86d025f8d0b576380058d8b00180349db46bafbdf6eaf8e4934ffe71c30d375cb97efd
fa7fd89030c5e2775a1c20088130a6edc85258ab4380d300563074f04fe9eeee86694c
040b0500abaf13362e06e1a399b0089fb92d6e7f7fffd0d6ad5b070f38e0802356ae5c
f9bf575d75d5659f7ffef9bb163fb50c82b0f7877e4fb8cd7e41741623e1e26211788f
d949660b6fd00249165098e99c3c7972cfe6cd9b4b93264d5ab862c58abf2e5bb6ec04
13fe6e4060f17406a729cc159fccdb9e262b00688d1a2710d0f056354a5b7009e1cbe0
470b8480000826fcae9f7efaa9d4d3d333d740b0aab7b7f70f0108e8108500412b0010
8f040068e5414f74c7cd0d27a5a15f15020c80c03441d7d75f7f5d9a356bd65c9b14ae
3cf0c003ffb96820685560712dc0927064ec2cbadf26b72c711ab5c781c034c0bc871f
7ef8c93208facbc341db6b825601a04e812b30846185f40bb8aabc9e050601837826bd
bffefa6b575f5f5f69c992258060e5d2a54bffc934412140d02a002a83a5b855601741
874682972bc1872e0018181888b66fdf4e6f2f2d5cb870fe430f3db4d2c0b0bc082068
150021bf0aeb97e0e5d210848c91f0e5128e3f04017e5b1544d3a64deb3230a009163c
f0c0032b162f5e7cac8160c0e2591db4e57030010027662f68bc0853067f28ecd04f1c
bd1fd7560291ed0aba6c3366cce8b2bd8292cd0916dd7ffffd2b4d231c6313c610049a
3457ab1b153ac66ea5b5635c703b1787a031b8718bc043cb061100601830c1477befbd
f78826b0fd81c5f7dd77df8af9f3e71f5d0601ef0fb4692620b8b2c6eb275700c49955
b467044b9de5cacf3382c6ca2f97303401c6de154453a74e8da64c99e2408026b0edf1
2580c05e941d692018b47c6d05825c01305e28ceb35c848e41c09810c484c90a0c3ccb
bf63c70ef6061c0000c2f4e9d3dd7070f8e1872f35103c3977eedcb603c104009c98ab
7f0402b92110e417107049878b06401b0002acbd341a0181bd2905042be7cc9973443b
6982dc0110f698a2fb43e1aa2deaed02809e7177efdeedc060dbc4239a0010b03a6038
38f2c8237bdb0d04b903a0ba2f15f70981631034460048724903000607790bee378798
186a38084170f4d1471f5806c1e1eda0092600e04456ff476008854f8ef019bfadf9dd
3b02c0c0502010000081c0b444a99d40d0360008dfc0d517c7d8c54af0127658b2e204
02b480f568f7d690309e1b80e0a076d0046d0100bd6a0d19dcae7e095ca0d0332e4640
ae07025607654d70109b4536311cb7e1207700840c69d62f00349bbe1dd3d1e3a9978c
ea584b13b40b087207807a8018d1c88551a84e265021031be51bcb780953f5d33375c0
8f90e300509ce2c3e1808d22e60402c131c71c336e9a20770064110c9327cda0b3e41f
af3c714030f9939156d3336989d7c430dc27b0fd831220b01748633e1ce40e001a9ac6
d273a401d48bd2e46f97b4d41d01e362c27a290ee1cbb257801fd7de1fb8394119042b
66cf9e1d9f134094f1a532c650480e267700a4a913bd0446a1017899823fed1092a6bc
56d3523f99b85f82b7c3211c1089366dda14fdf2cb2fce6ed9b2c585eddcb9d3b58fde
3f73e6ccc804edecbefbee1bf116d1b6924b471d75d4b2071f7c70854d0c0f0bf60946
ed55725b1ce294061073dbdbf51a8e3a02020181decf56f0cb2fafb657c3bf4676749c
43220ed84a4b1ae6028cfff8ed055164ef07a259b3f63740cc88162c58e04e162d5fbe
7c19ab831b6fbcf1723b78fa99816b2fe311df1d840770423f456432e30e00188806c0
8a99995a3246993a3a3cdf257c5c7a7f67a71fe3bbbbfd30e0e3a9d4b0b5cd7f60421b
013bee0f3ffc605bc47b1b207a1c186c4218d96be3a8b7b7b76bc182f9a5934f3e79d9
238f3cf2e4d5575f7da97d96f6b995c1d757141e7e7bd93208c60c00c1496b53835e5a
b8c60fb3fe94adf7d3b37c7c3bfc8675f5f565d5a27a5343862d2acc32d0dbce4e40d0
65cfde020a86b6ee6e1a4e5b87590198da9fe9e6010082b3045f7ef965641f99988698
dab570e10203c12907fde52ffff53f575df56f97d8b0f2ad816ab2d1e133344000310a
2e73d37c194cee0000f99890715ec05ed0d6d6b2c049336c8c2a99ea1c3255391c6dd9
420fa16ded8300cd49bc2ba0b26c1d7675c6b577402640de067698cb3b01be8e9a64ed
c3f29189638903361a808f8ae9f97c4b333cdce380d2d3c31b44df6e3b4516ad5bf77f
5d6bd77e513af1c43f1c7ed75d77fdf7adb7fef9f25dbb766e31fef6184d8fa416854f
ad7207806f6abddfeaeff03c83aabfc449caeddb9c14d37c98c0d94c0e951777112080
aed4bb428d5e6f5f8ebb993de33cf2e9e90104ee8b2297d0e71f32a0f4b9c323dddd8a
67422c5a936d653095f943d75b6fbd3578f0c1cb4ebceeba6befbef7de7bafb7144cdc
2108084438b316c81d00494c26acbc3ab23a7b158f1aedec1c760c83698ca32c890607
2b132b97b8fcc392a9c2a030a6393f424bb3d7c024adabcb2f924261ab0733aeb37219
1c1c30b7dfb400cbbacad20e3fb3fd818141038c7f47e0e9f8f9c0c0c0761b02f6b13c
930d201ad6d5b149efe745364fe8deb8f187d2e2c58bff74d65967ad79f9e597ffb33c
1f1008320b1fce8d0a002a0c6302e41bd2df0fa33837873b688cf3e1a8fb81815d4ef5
6fd8f085eb59a148010ff93efae8a391f7ed617c337e04c0b2cbdec7ef413f9e9fba33
535fbb766df4e38f3fba091a6115a3decf10266dc0c40ebf9fe4d1b669d3a6ba3219db
bdc6505a2fe42953265b9e5d4683eb05e80c74123fa10478a6e9cd4e72342d6de7ae5d
bb2303c09f3ff8e083576d65f095f1a5dbea158e9761252bd56de0cb1d006216bdd5f7
581ae3fd3d3d9dd62bba1d28c4147afed6ad8ca3fdd1fefbcfb0064babc16034445764
1f5d441f7ef88e130c9a406534689b8b863ecb310070da692755d14fca0f6db66a5f7a
e90b1b87d745acd10171c5a0a12a4ff842ad077858f7b3bc3bf2c8435dd9e007ba00c6
fb876c9f60b36980e96e12e8dbe3014087080dfc30dbc16ea1d56bded9679ffdaff62d
e2bf5b99932c1f07103ca2c24c29fcb90340657ba6b034f20724085758c840040a183a
3afa6c1dbcd0f5769fce330d86b2b1326dda7427448609cf309554df05400804a1b2cc
a2a7d633309cf37cccd0599f23c8a4a10341568c7fa05e6acff4e933a2850b1739f0aa
beb8f203f879f3e633e3b7f6bbbb071c392f70269b5e43f20c00ad4ec6968ec8f608ce
5cb56ad5fd16d66719b443485e9053552b021b99dc0120e18505abd17215c733e97da3
fd0b21982d1a4a4f184c409d62142e3af55c00c0100270341ed74b4f5d484f797ec8ea
4f04403d1a6a03601060a9b3da8bcbfc00cb5040998a87aef84198fc46b383b61820e7
1b98f733adb6c3f8c4d53cba8c23b5f0292b770040346e24d07838cfc42559a5ad17a7
34f55ce5270dc3014cad67c2f4f2e3366b9496b2d03a8001132f973859c5e18656c227
0c3a00ca76183bcdcf3d0ce1f6b02b23cbcf9800204bc58a9e87deea570195771c1234
2041330800085a466908c32f10e0428f7c0600e416022093faa7ccdc01a01ea0063572
499f64954f713cc31059c53772c3f421ad5af994065779719b35ca437e8485152dd120
0dbd59360480d28a8e5cd20018e85918c247fd877300914fe5e60e8054a5ff46132334
3400026612cb7080215c46c247a0cc374213a6c32f2d409e32a0e8f1dcc5d011a60d69
34eb2f0c005a6d68b30cc9331dc24768f46a19dac1b3e242809046ed0c5dfc804000b0
64101451b9644f6d0a03005a0623649b6d69daf471ba69f32b3d42a6e7cb121e1ac5a3
29428090264c2b3f00a0f793de4c5ce8f167d234657205000d8937a6512d9427ee2a5f
182ee68a294a53cf559e904ebdf4a40b55368ccf5a1ec2c28a9eca859ee2702953262c
cb63a6029c182d3255328a404a375700345376d056973c7cc62f2b5a7a0e19a3b874ae
7fd9129697945fe5299ddca4b4f5c204246df156a7f51d852ddf247054a7f54fd063b8
0004799adc0110a259150db59f75a8114338f31fc5e3c78ae984e3d71c0910c88e1069
e0f15bcee48b6cf9c4264bfd0cc4938e77fc94a5fcf573556243a042cb76712d72cf8e
8ae07d19fe3c81da9cc43fab8dd312c425c757ca4febcb1d00aa000cc7e0c2448488eb
995271bbba3a46ce036cddcae9e0cac9209849bcddbfe4e8646bbc671ee5fffaab7f33
e76b96fccb7e3d3b860303fea6d0e454f54311a66d26daa64dc9de0594ac9797991164
830f7d7dec7efa6d60f2b058a0bdb85e73789776fbb03d354699e49e050465d5f38e1a
006a174a5d7d7de3bd19801057014f758f57fab097d52ec7c7280f4fa1bf56beea34d5
e5d7ca138657f2371e72103a16237fe599deae70b4844f97f7ef9800c0ab2e1ae3911c
36d89f056022e4efda41fdaaa7c34ce2fde9998a00096fd64820d0e4f0853f71543b37
1a8074d44779b395c73171cefbf558eff5fb0061a9d487b6110f7dce1a227092e2ca2a
0fe9651596879b3b0068ac9f39fbd9336fdf5073fec54ae54c0061fe2d58edf3003086
49cf8e1ddb1dcdac0d469d0e0cec8ebefffeab86742873d2a4c9362c6d3786ef29b846
75203f278376eedc166dd8f0a5b93b1201502a0d46f6170416d7ed844d3b393b386992
df21c4c58633ff4200000660c2ca826626af9c072895380f404ff40724008cbded7587
3d66cf9e59252001a0af8fa554f6ad598616981b3f6f90244ccae40d1de716b404549b
92d2c7c3484bbec993274573e6ccb439406527304cbb71e3ce689f7df6766063d8830f
582f70bf7cf47edff3cb6c0d49e4e2cf5d0320788c5c1a21e3c3fcd866292cd8ef897b
066f73efcfd114ca4b384b1fced8c31c9e6545b3914b7a04c22e1ae70de2dbaef1fca4
f5173ded950900d0130ddef7736f10758f9b9f7ffec500399bdb43ac4e2c4d7cc7a1be
98b80bcd902f2e510e3fb903205e27358470fcf167c2691ce1083f0e00c279151ae623
4f5a23facd00803a50a7560cf975a62009006a57bc2c09b995b2d3e41d7500c42b136f
60f88c5f56f9c2679826abf8466e983ea4552b5f3c4d98bf569e303c4c2f5ab849a651
7c521ec26ad1ab95be5ef89ebaa95eea89b8df1c0772d70069d119f682d02f4e2b8c67
f52edc664d9836a4552bbfd2e0b6525e48077fdc348aaf973e6c533c5ddae7dc0190b6
0269d2671508f99284d0a8ec56ca6b44bb5de27307405a46c77b829ec5a0f8b3c2b3b8
cdd06a264db3658b166edc847149f1f5d2c7e35a79ce1d00ad54a651deb1ee9159cad3
8aa6515bda253e77003483e6b0f1f19ea067a5893f2b3c8bdb0cad66d2a429bb163d85
cb6d44b3d9748de8c4e3730740bc803c9fe95d597a1879d21a188e065099cde6573edc
229889656011a4348a752c9406c832269327abc95a5e2b6566ad6bd67cbf0b0d502481
641564d67cb96a802c1315e589bb6a50389666ed9121ad909ec24357f55098cad47323
57e9f98a0713a7a7fc0a97abf05aaed2e1e6697205409e15132d18ca9b3cde0a720b97
18acf846aed267619cf2e2366b48cbc451006836df78a5cb1d0069192d64c300f94503
1786ea1b3aee09287f1ad534bf2444ad0444bb1601c5ab6ce5af953e1e2e0070091406
3aa2194fabb85af1617aa5911bc6b5e26ffb39000c4503d8458aeeb57096c6f23a964b
1ac357cdb5e8c060ca44dbc85f2b6d523879c9c7c512453085000002e4564dce056060
72b3969ecff0a11b3c39a042de5a06e101166ef9245fb3e5281d6700c8b7fffefbbbbc
d0cbd3402f4f9a6d0f00316fd1a245ee808518ddac0b00103a7fecf8d5575f39bf8603
d1964b3843cc77df7d17d93d3cce8f409b2d0b3a68194ef9008046874f54ee78bab903
4008cdcbd5699aa54b978e08240bc310ecabafbeea26680c2971c1227cd579f5ead54e
db84c7d99a2993fc0c1d5c45b3cf3efbb832a8bfe8b6eaaa0e00322f933b00f2aa98e8
c0347a151a8061201c9b9bed99089b5ef9c5175f448f3ffeb8d302fedcdf14375b6792
c9bd7eb8cf3df75cf4c61b6f8ccc399a2d4342e11a1bfb9f40277485a92d79b8f0234f
d336ab8078ef081b49ef44385cf3f6d24b2fb9439b617c337e687053185a60fdfaf591
ddc51bd9dd7b8e96fd7d4bb471e3462778aea363064f7dd20a90390acb3ffb53285725
f5fea4fad56b6fadf449e1ad86e50e80562b542fff89279e18bdf2ca2b2393c17a696b
c5a19abffdf6dbe8b1c71e73430a6a1e700002266f8004c11396c6206c96a9871c7248
d4dbdbeb2eb4cabbb7529fbc691602003017d56a7fc61cd93f70469f7cf289eba56985
0403190e50fffcc9733849230c938526f9000d43d519679cc1a37bce5b588e70ce3f6d
3f07507ba58ecf3ffffc4c3d5474701172287c8565153e00659571d8618745c71f7fbc
032b614530c5a8a5711286a2a6d100a79e7a6ab479f3e63d3e160124636d11b2f6272e
bef8e2913a8da6f0f3d42c8501000ca5e1f4dc4b2fbd343ae080035caf0318632df4b0
3cea04182fbcf0c2c8fe2ade81b428bd1f9ee60e0018325a16c60200c6efebafbfde2d
ddf8f42aed7a9d86e76128971dc3d34e3b2dbae8a28bdc1c80b0d16a3f7586769e2677
00e459b9245a808009214bb85b6eb9c52d0f197fc752134808f6572e6e39697febb2c7
9c22a9eeed18963b00eaa1bf1e03c4d47a691427101c7cf0c1d11d77dce13689e889a8
66e246cb5047e8f3ae80770ba8fd6bafbdd6f54a269069dad0282df171ab76d1cebccc
a82f032b0df59743549efd528986c05485b31697bf512361c4c2850ba33befbc337af6
d967a3bffded651b8377b8cd185471385637a29514af7ae89e0096794c44172f5e145d
7ef9e591fdc5db08e8d20e43d0260f6d8f8356f5a64e5ed6f9093cdece5103801ac198
8d8579b2fccb46b814dbb973979b49f3a749e44b63b8d10346fef18fff62d7bbef17bd
fefaeb6ea7afaf6f9bbd46f657b50a60213343bf2f8f1e57f6953dfe6e23fee4823f7d
1872fbfbc71fbf3c3ae59453dc86d1dab59f9585977e5c86e637df7c6375f480a78eb4
83f714b2fa4731e2c417802360a6e153adb4a306800a5351c9085545c12c7a273b6da8
4de2ed06274bd3d1c1664cba1d3864c5a6ddb66d25db283ac666e2c7b937796bd77e1a
7dfae947b6c5bbc12e69e8b3340c0fbed7516635232bcb47fdf30700f13b83fbdad2f3
40db863e3662878f092843405fdfa0096c9ad5379be1ff11ec4fc02cb33f3ae6e7e3f0
82fb14e0159667f85501a73de46a24955c897a62bed25c97c2ed1c066243b617160283
c108857b7230bb766db357a80b9c26c88a70699ddede7d0d0c87da5fac5c60d7b0fc68
57b57c63d7c36c70fead5b37bb2b6758bba389bc06e1ae9e6e37744c9b36c30e73ec67
f7f2cfb7b77a8bcd2eb29e3fd381a7bfdfff25cc94299cf649dfeb5d43cb3f7d7d9bec
85d36c5bc9ecedea0090b1a6041cafe01756e1d200218d3cfca30880b07af43084ce1e
bbae8ce3998b21f8c30818eb2f8240285901a012eddf55cc8b46e9b46b5ae6bb9b41a4
2906061892fc70c43d3dd4817b7ae8eda85c5caeb2c10054ae8c6388c2a85e84e76128
1f20fa3a54cf91280b9ea9cc3cca4ba2913b00922a0c924383303c2018f7643b8cf1ac
a1d3cda643ba7bfa01dea08de1c6490708988ce532a6eac9a6b407e977ef9684fd784b
dabc0d7ceaeee66634c677dfd37daff740f0f5f400805fe6cbbb0a8e5efe2d2b57d357
da378ccaa3da7a7aaa1b01d3b91871c70edec875994a64a7affaeedc5169b523eab592
e87be0c690aac8517011fef4e95d36a7a0edd57c492a0e908c86193500a4a92ccc67a6
3bb666f42656cdb423cd72b7197a59d3e40e80a421a051e5fcb8cb5fa94ae535ee118d
68b67b3c4b3d81be199e290d6e9e13c2b1ee768972d1fa3731f2371ac8194509753c9b
38ae0010034200286c3c993216657374ac1dda3aae0010a3430028ecb7eea20134048c
675b739f0364694cbb4c88b2d43d6b1ee60068803cc7f32c7519770d000360045a60bc
9991858159f3b40be8db4203a00a7f4fc20734eda0fea947ae00d0a4462e053463a40a
d3e66b8676bba641e3a5696f9ab469da9c2b00d2141c4f3b5a0d8c9793f539d45079d4
350f1a59db12e66b1b0084956ad62fa124315371d00ae3c3f0a472e269390780ba4e0a
a71717dd141a00a150e282a815572b3c9e5f4041c88080af7e38d0c23784d870d2da2c
cd7819edf05c3800a8477ef6d967d1ca952b1d0f399ec54719c4210c2c71efbdf75e74
eeb9e7dab980b35cba0f3ffc305ab56a953bd4e15fc3fa372cf4f0eddbb747279d7492
3be7c7092604ccb9bfe79f7f3e7afbedb7dd27e31c07e3bbc1dededee8f4d34f770742
290bb01415048503807acd962d5ba2b7de7acb3d9e77de79ce0d05b176ed5a773c8c2f
756538c5fbe69b6fba2f7ff9d894a51879246c048be1990f48efbefbee68ddba75ee1b
423ef8dc6fbffda2afbffeda7d44ba66cd9a087bd34d37b9f8b06c955704b7b0004048
1ccfc2e0c784bd1001f349383b6e32089c1e4cd8adb7de1a1d77dc71237fe9820089c7
a00deeb9e71ef711e9bc79f3a29b6fbed9a595909f78e289e8e9a79f761faa5287ebae
bb4e4514ce1df78da0ac1c4318a87c2cfeb8517c18a730f20010810821021676e7302f
bcf042f9c0664f74c9259738e1332c901f7bc51557b830f6f3f9dc9c9b47001f748b66
0a0b80d160b43667de79e71d37f347e5738f008638ac84cc1c00a1736105430126049b
0b28c04f618780acbc4548088e0b2166cd9ae50448185a60eedcb96ee2c75c81309eb9
2f00a3e1452059ba74a95b0df055d2860d1baad2b88782fcfc2e0180aabfefbefbdcb2
8e719fd93e2b053e30a147b3dcc3688e21d0843245fd6b7e411e8c4012a66b77ffef0e
000889f1fc0cbbc8811ece72908f340e3ae820272b84aac9201f9ed632e41150000326
0928b5f2b74b7861018020b18cc908346e100626de2b058073ce39c7dd39447ea975d2
73850c973c724d1c960d20268812ae5cd43e1f8860b8150ca332dd43417e0a3b096439
474f4580080aa3cd1d04c13e0182951a8fcb43a0c1c542078b39f6d8639d9fb9802678
4a2721bff6da6b2e0dc3c9f2e5cb5dbe38d85c609bff140e0062f292254b4626685ceb
c62e1dea1ba17ff0c1076e0d8f6aee2d6fee2007f2caaad7b314c4f22cda5c433367ce
1c07a8279f7cd26dfe0036e249fbe28b2fba0d258681134e38c1dd5a023044b3cd655e
55bdc20d0108819eca7efc65975de626736cf1de76db6d6e6dce260e1f88a21518e7e9
cdf45e0487ab099b7a7bc80dd16608e0ee017602f980934fd0d926269c0f58d96246db
409b8b2a8a6c0a0700984d4fa3c79d79e6996e678f5d3936633efdf453276876efaebc
f24a77954c281cc67234029a828da02423da7cfa0d009e7aeaa9e8fdf7df77f7132274
6e13e3b632f6072eb8e0024787ba487b24d16ce7b0ac07f0c9876508996c4c9b6e3d6a
8a5de478d6c71f7ffc88853103cb4adbb23667c4787a33f7f4b0264755b3be474328be
396ad5a9a08950b1ac06366ddae466fdcc29d820a21ce863c642f8569f61e3738769a0
9fec2ea23fd9f37a2b779bd561bb55a1df2c13983db7442db09e6955038cba90eb551e
c64b50081d2ba3703da775d104d040c8f47add23283a0c27a4190be1abcc3a6e6639b4
0a803a751a9b2884804150618f54782bb5108d386d84ce9ce2b7605a0540a872f087cf
63ca1f84325abd713469676492782d7ecb4d4dae5500a8402a30643d6508d5886bcf99
d592884eb8150ed870346c93d72ee32fbb5e99c6fb0ab58aaf15000875b8d892f594a1
b26a442f4f00a0c2e7967d000022c6df4ee33320f0b760b4a875b30280ca20605c7a3e
ffe5d26dffb4f1dd35d75cb3c29ed91ce7240603e504188c092d18f178c0561e43b6da
f9dec0c0ccbf647c160832936fa5979217e1022204cef11c2c0bec1966b9f189f00910
1813321a277ccbcbebc9dd66fbcc6e0bfcbcad225c40207d2a935503a81055100db0db
5453b7a92868f27e94718aca0100014dae054d98061c9030e123020604fdf47a33f097
b5bf046fde6ca6158128afb400e7a950fbf47a2c40c0924e69cd3b61527220ec640e04
969f8e85a5e30182cc93c25634001543b0b8540223bf7afec4f8eff9d2ea2f02962680
d7085ec287e7994dab3d53f971b1085c2a1f3f4669fcd3c46f160e2064598141bd5ee1
59e8e6221c093874437fa68a4d64da8303a1a0e3fe3d12371b2041359bbe5eba38adf8
73bdbc1371cd7100c18726fe1cc635e5ff7f6d102cb21055ee1c0000000049454e44ae
426082
""".strip().replace("\n", "")
testImageData = b"\x89PNG\r\n\x1a\n" + testPNGData.encode('utf-8')


class TestImage(unittest.TestCase):

    def getImage_generic(self):
        image, _ = self.objectGenerator("image")
        image.data = testImageData
        image.transformation = (1, 0, 0, 1, 0, 0)
        image.color = (1, 0, 1, 1)
        return image

    # ----
    # repr
    # ----

    def test_reprContents(self):
        image = self.getImage_generic()
        value = image._reprContents()
        self.assertIsInstance(value, list)
        color = False
        glyph = False
        for i in value:
            self.assertIsInstance(i, str)
            if "color" in i:
                color = True
            if "in glyph" in i:
                glyph = True
        self.assertTrue(color)
        self.assertFalse(glyph)

    def test_reprContents_noColor(self):
        image, _ = self.objectGenerator("image")
        image.data = testImageData
        value = image._reprContents()
        self.assertIsInstance(value, list)
        color = False
        glyph = False
        for i in value:
            self.assertIsInstance(i, str)
            if "color" in i:
                color = True
            if "in glyph" in i:
                glyph = True
        self.assertFalse(color)
        self.assertFalse(glyph)

    def test_reprContents_glyph(self):
        glyph, _ = self.objectGenerator("glyph")
        image = glyph.image
        value = image._reprContents()
        self.assertIsInstance(value, list)
        color = False
        glyph = False
        for i in value:
            self.assertIsInstance(i, str)
            if "color=" in value:
                color = i
            if "in glyph" in i:
                glyph = True
        self.assertFalse(color)
        self.assertTrue(glyph)

    def test_reprContents_glyph_color(self):
        glyph, _ = self.objectGenerator("glyph")
        image = glyph.image
        image.color = (1, 0, 1, 1)
        value = image._reprContents()
        self.assertIsInstance(value, list)
        color = False
        glyph = False
        for i in value:
            self.assertIsInstance(i, str)
            if "color=" in i:
                color = True
            if "in glyph" in i:
                glyph = True
        self.assertTrue(color)
        self.assertTrue(glyph)

    # ----
    # bool
    # ----

    def test_bool_data(self):
        image = self.getImage_generic()
        self.assertTrue(image)

    def test_bool_no_data(self):
        image, _ = self.objectGenerator("image")
        self.assertFalse(image)

    def test_bool_data_len_zero(self):
        image, _ = self.objectGenerator("image")
        try:
            image.data = "".encode('utf-8')
        except FontPartsError:
            raise unittest.SkipTest("Cannot set zero data")
        self.assertFalse(image)

    # -------
    # Parents
    # -------

    def test_get_parent_font(self):
        font, _ = self.objectGenerator("font")
        layer = font.newLayer("L")
        glyph = layer.newGlyph("X")
        image = glyph.image
        self.assertIsNotNone(image.font)
        self.assertEqual(
            image.font,
            font
        )

    def test_get_parent_noFont(self):
        layer, _ = self.objectGenerator("layer")
        glyph = layer.newGlyph("X")
        image = glyph.image
        self.assertIsNone(image.font)

    def test_get_parent_layer(self):
        layer, _ = self.objectGenerator("layer")
        glyph = layer.newGlyph("X")
        image = glyph.image
        self.assertIsNotNone(image.layer)
        self.assertEqual(
            image.layer,
            layer
        )

    def test_get_parent_noLayer(self):
        glyph, _ = self.objectGenerator("glyph")
        image = glyph.image
        self.assertIsNone(image.font)
        self.assertIsNone(image.layer)

    def test_get_parent_glyph(self):
        glyph, _ = self.objectGenerator("glyph")
        image = glyph.image
        self.assertIsNotNone(image.glyph)
        self.assertEqual(
            image.glyph,
            glyph
        )

    def test_get_parent_noGlyph(self):
        image, _ = self.objectGenerator("image")
        self.assertIsNone(image.font)
        self.assertIsNone(image.layer)
        self.assertIsNone(image.glyph)

    def test_set_parent_glyph(self):
        glyph, _ = self.objectGenerator("glyph")
        image = self.getImage_generic()
        image.glyph = glyph
        self.assertIsNotNone(image.glyph)
        self.assertEqual(
            image.glyph,
            glyph
        )

    def test_set_parent_glyph_none(self):
        image, _ = self.objectGenerator("image")
        image.glyph = None
        self.assertIsNone(image.glyph)

    def test_set_parent_glyph_exists(self):
        glyph, _ = self.objectGenerator("glyph")
        otherGlyph, _ = self.objectGenerator("glyph")
        image = glyph.image
        with self.assertRaises(AssertionError):
            image.glyph = otherGlyph

    # ----
    # Data
    # ----

    def test_data_get(self):
        image = self.getImage_generic()
        # get
        self.assertEqual(
            image.data,
            testImageData
        )

    def test_data_set_valid(self):
        image = self.getImage_generic()
        image.data = testImageData
        self.assertEqual(
            image.data,
            testImageData
        )

    def test_data_get_direct(self):
        image = self.getImage_generic()
        # get
        self.assertEqual(
            image._get_base_data(),
            testImageData
        )

    def test_data_set_valid_direct(self):
        image = self.getImage_generic()
        image._set_base_data(testImageData)
        self.assertEqual(
            image.data,
            testImageData
        )

    def test_data_set_invalid(self):
        image = self.getImage_generic()
        with self.assertRaises(FontPartsError):
            image.data = 123

    def test_data_set_invalid_png(self):
        image, _ = self.objectGenerator("image")
        with self.assertRaises(FontPartsError):
            image.data = testPNGData.encode('utf-8')

    # -----
    # Color
    # -----

    def test_get_color_no_parent(self):
        image = self.getImage_generic()
        self.assertEqual(
            image.color,
            (1, 0, 1, 1)
        )

    def test_get_color_parent(self):
        font, _ = self.objectGenerator("font")
        layer = font.layers[0]
        glyph = layer.newGlyph("A")
        image = glyph.image
        image.data = testImageData
        image.transformation = (1, 0, 0, 1, 0, 0)
        image.color = (1, 0, 1, 1)
        self.assertEqual(
            image.color,
            (1, 0, 1, 1)
        )

    def test_get_color_no_parent_none(self):
        image = self.getImage_generic()
        image.color = None
        self.assertEqual(
            image.color,
            None
        )

    def test_get_color_parent_none(self):
        font, _ = self.objectGenerator("font")
        layer = font.layers[0]
        glyph = layer.newGlyph("A")
        image = glyph.image
        image.data = testImageData
        image.transformation = (1, 0, 0, 1, 0, 0)
        self.assertEqual(
            image.color,
            None
        )

    def test_set_color(self):
        image = self.getImage_generic()
        image.color = (0, 1, 0, 0)
        self.assertEqual(
            image.color,
            (0, 1, 0, 0)
        )
        image.color = (0.5, 0.5, 0.5, 0.5)
        self.assertEqual(
            image.color,
            (0.5, 0.5, 0.5, 0.5)
        )

    def test_set_color_invalid(self):
        image = self.getImage_generic()
        with self.assertRaises(ValueError):
            image.color = (0, 4, 0, 0)

    # --------------
    # Transformation
    # --------------

    def test_get_transformation(self):
        image = self.getImage_generic()
        self.assertEqual(
            image.transformation,
            (1, 0, 0, 1, 0, 0)
        )

    def test_set_tranformation(self):
        image = self.getImage_generic()
        image.transformation = (0, 1, 1, 0, 1, 1)
        self.assertEqual(
            image.transformation,
            (0, 1, 1, 0, 1, 1)
        )
        image.transformation = (0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
        self.assertEqual(
            image.transformation,
            (0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
        )

    def test_set_tranformation_invalid(self):
        image = self.getImage_generic()
        with self.assertRaises(TypeError):
            image.transformation = (0, 1, "a", 0, 1, 1)

    def test_transformBy_valid_no_origin(self):
        image = self.getImage_generic()
        image.transformBy((2, 0, 0, 3, -3, 2))
        self.assertEqual(
            image.transformation,
            (2, 0, 0, 3, -3, 2)
        )

    def test_transformBy_valid_origin(self):
        image = self.getImage_generic()
        image.transformBy((2, 0, 0, 2, 0, 0), origin=(1, 2))
        self.assertEqual(
            image.transformation,
            (2, 0, 0, 2, -1, -2)
        )

    # ------
    # Offset
    # ------

    def test_get_offset(self):
        image = self.getImage_generic()
        self.assertEqual(
            image.offset,
            (0, 0)
        )

    def test_get_offset_set(self):
        image = self.getImage_generic()
        image.offset = (1, 4.5)
        self.assertEqual(
            image.offset,
            (1, 4.5)
        )

    def test_set_offset(self):
        image = self.getImage_generic()
        image.offset = (2.3, 5)
        self.assertEqual(
            image.offset,
            (2.3, 5)
        )

    def test_set_offset_invalid_none(self):
        image = self.getImage_generic()
        with self.assertRaises(TypeError):
            image.offset = None

    def test_set_offset_invalid_string(self):
        image = self.getImage_generic()
        with self.assertRaises(TypeError):
            image.offset = ("a", "b")

    # -----
    # Scale
    # -----

    def test_get_scale(self):
        image = self.getImage_generic()
        self.assertEqual(
            image.scale,
            (1, 1)
        )

    def test_get_scale_set(self):
        image = self.getImage_generic()
        image.scale = (2, 2.5)
        self.assertEqual(
            image.scale,
            (2, 2.5)
        )

    def test_set_scale(self):
        image = self.getImage_generic()
        image.scale = (2.3, 5)
        self.assertEqual(
            image.scale,
            (2.3, 5)
        )

    def test_set_scale_invalid_none(self):
        image = self.getImage_generic()
        with self.assertRaises(TypeError):
            image.scale = None

    def test_set_scale_invalid_string(self):
        image = self.getImage_generic()
        with self.assertRaises(TypeError):
            image.scale = ("a", "b")

    # -------------
    # Normalization
    # -------------

    def test_round(self):
        image = self.getImage_generic()
        image.offset = (1.1, 1.1)
        image.round()
        self.assertEqual(
            image.offset,
            (1, 1)
        )

    def test_round_half(self):
        image = self.getImage_generic()
        image.offset = (1.5, 1.5)
        image.round()
        self.assertEqual(
            image.offset,
            (2, 2)
        )

    # ----
    # Hash
    # ----

    def test_hash_object_self(self):
        image_one = self.getImage_generic()
        self.assertEqual(
            hash(image_one),
            hash(image_one)
        )

    def test_hash_object_other(self):
        image_one = self.getImage_generic()
        image_two = self.getImage_generic()
        self.assertNotEqual(
            hash(image_one),
            hash(image_two)
        )

    def test_hash_object_self_variable_assignment(self):
        image_one = self.getImage_generic()
        a = image_one
        self.assertEqual(
            hash(image_one),
            hash(a)
        )

    def test_hash_object_other_variable_assignment(self):
        image_one = self.getImage_generic()
        image_two = self.getImage_generic()
        a = image_one
        self.assertNotEqual(
            hash(image_two),
            hash(a)
        )

    def test_is_hashable(self):
        image_one = self.getImage_generic()
        self.assertTrue(
            isinstance(image_one, collections.Hashable)
        )

    # --------
    # Equality
    # --------

    def test_object_equal_self(self):
        image_one = self.getImage_generic()
        self.assertEqual(
            image_one,
            image_one
        )

    def test_object_not_equal_other(self):
        image_one = self.getImage_generic()
        image_two = self.getImage_generic()
        self.assertNotEqual(
            image_one,
            image_two
        )

    def test_object_equal_self_variable_assignment(self):
        image_one = self.getImage_generic()
        a = image_one
        self.assertEqual(
            image_one,
            a
        )

    def test_object_not_equal_other_variable_assignment(self):
        image_one = self.getImage_generic()
        image_two = self.getImage_generic()
        a = image_one
        self.assertNotEqual(
            image_two,
            a
        )

    # ---------
    # Selection
    # ---------

    def test_selected_true(self):
        image = self.getImage_generic()
        try:
            image.selected = False
        except NotImplementedError:
            return
        image.selected = True
        self.assertEqual(
            image.selected,
            True
        )

    def test_selected_false(self):
        image = self.getImage_generic()
        try:
            image.selected = False
        except NotImplementedError:
            return
        self.assertEqual(
            image.selected,
            False
        )
