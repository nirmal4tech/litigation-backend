INSERT INTO case_types (slug, title) VALUES
('divorce', 'Divorce');

INSERT INTO stages (case_type_slug, slug, title, short_desc) VALUES
('divorce','filing','Filing','Case is formally filed in court'),
('divorce','service','Service & Response','Notice is sent and reply is awaited'),
('divorce','mediation','Mediation / Counselling','Court encourages settlement discussion'),
('divorce','interim','Interim Applications','Temporary issues are considered'),
('divorce','evidence','Evidence','Documents and witnesses are recorded'),
('divorce','arguments','Arguments','Final arguments are heard'),
('divorce','judgment','Judgment','Court gives final decision'),
('divorce','post','After Judgment','Execution or appeal stage');
