-- UPDATE client SET profile_image = 'octo.jpg' WHERE email = 'jngugi31@gmail.com';
-- UPDATE client SET profile_image = 'nyashinski.jpg' WHERE email = 'muimikieleko@gmail.com';

-- ALTER TABLE client MODIFY COLUMN profile_image VARCHAR(100) NOT NULL UNIQUE;
-- ALTER TABLE beat DROP COLUMN prev_address;
-- ALTER TABLE beat CHANGE COLUMN `address` `beat_file` VARCHAR(100) NOT NULL;
-- ALTER TABLE beat MODIFY COLUMN beat_hash VARCHAR(100) NOT NULL UNIQUE;

-- UPDATE beat SET beat_file = '01_Friend_of_Mine_feat._Vargas__La.m4a' WHERE beat_hash = '97deb4653ac2ea8ea2261f4e74a17c64';
-- UPDATE beat SET beat_file = 'Rules.m4a' WHERE beat_hash = '76bd8d62b7533d16d6da70a443919449';
-- UPDATE beat SET beat_file = '02_Revenge_feat._Eminem.m4a' WHERE beat_hash = 'ce8e447fd2b8afa9cac11411019d53a9';
-- UPDATE beat SET beat_file = '11_Apparently.mp3' WHERE beat_hash = '1fc971af66a0b9087e357e8ef5c13fba';
-- UPDATE beat SET beat_file = '02_January_28th.mp3' WHERE beat_hash = '4279a8e5fadbd7817396c3e3f793f18f';
-- UPDATE beat SET beat_file = '06._Daddy_Lessons.mp3' WHERE beat_hash = 'de52f4942be5c29d644855b89a24237f';
-- UPDATE beat SET beat_file = '06._LOYALTY._Ft._Rihanna.mp3' WHERE beat_hash = 'af642eb0ce0238e1c98f40a73d3a57e0';
-- UPDATE beat SET beat_file = '03._Tribe.mp3' WHERE beat_hash = '606de09ee008e512c97212dffe548e23';
-- UPDATE beat SET beat_file = '06_Water_Under_the_Bridge.mp3' WHERE beat_hash = 'ad651688207a45e2dca913cc20e9bea5';
-- UPDATE beat SET beat_file = '14._Non_Believers.mp3' WHERE beat_hash = '2ca85cf8922cf2a245ed340a1339c946';
-- UPDATE beat SET beat_file = 'Khalid_-_American_Teen.mp3' WHERE beat_hash = 'bf1f25f4f3a5ba9153464921ca3b4831';
-- UPDATE beat SET beat_file = '02_Im_a_Mess.m4a' WHERE beat_hash = 'd6ff1a054dd0b2719048aee5323fa963';

-- DELETE FROM beat WHERE beat_hash = 'bf1f25f4f3a5ba9153464921ca3b4831';

