use test;

INSERT INTO Permission (id, name, description, page, created_at, updated_at)
VALUES
  ('perm1', 'View Report', 'Allows viewing reports', 'report', NOW(), NOW()),
  ('perm2', 'Edit User', 'Allows editing users', 'user', NOW(), NOW()),
  ('perm3', 'Access Lobby', 'Allows access to lobby', 'lobby', NOW(), NOW()),
  ('perm4', 'Process Orders', 'Allows processing orders', 'order', NOW(), NOW()),
  ('perm5', 'Manage Food Service', 'Allows managing food service', 'food_service', NOW(), NOW())
;

-- ============================
-- INIT ROLESs
-- ============================
INSERT INTO Role (id, name, created_at, updated_at)
VALUES
  ('6ac907e7902f4feb8da20becac50bedc', 'Admin', NOW(), NOW()),
  ('6ac907e7902f4feb8da20becac50beda', 'Staff', NOW(), NOW())
;

-- ============================
-- INIT PERMISSION FOR ROLE
-- ============================
INSERT INTO RolePermission (role_id, permission_id, created_at, updated_at)
VALUES
  ('6ac907e7902f4feb8da20becac50bedc', 'perm1', NOW(), NOW()),
  ('6ac907e7902f4feb8da20becac50bedc', 'perm2', NOW(), NOW()),
  ('6ac907e7902f4feb8da20becac50bedc', 'perm3', NOW(), NOW()),
  ('6ac907e7902f4feb8da20becac50bedc', 'perm4', NOW(), NOW()),
  ('6ac907e7902f4feb8da20becac50bedc', 'perm5', NOW(), NOW())
;

-- ============================
-- Create admin account
-- tk: test
-- mk: test
-- ============================
INSERT INTO `User`
(
    `id`,
    `display_name`,
    `username`,
    `password`,
    `role_id`,
    `created_at`,
    `updated_at`
)
VALUES
(
    '827cdd116faa437598a10adb739e20e2',
    'test',
    'test',
    'pbkdf2_sha256$390000$wd46Emene7YLBYvIfFzn5Y$kG5ex1J3TNMC4RIBTWybMlj4Du3Z4Zq5rqGee9DE6Bk=',
    '6ac907e7902f4feb8da20becac50bedc',
    NOW(),
    NOW()
);


-- ============================
-- INIT LOBBY TYPE
-- ============================
INSERT INTO LobType (id, max_table_count, min_table_price, deposit_percent, created_at, updated_at, type_name) VALUES
('1', 10, 1000000, 30, NOW(), NOW(), 'A'),
('2', 15, 1500000, 30, NOW(), NOW(), 'B'),
('3', 20, 2000000, 30, NOW(), NOW(), 'C'),
('4', 25, 2500000, 30, NOW(), NOW(), 'D'),
('5', 30, 3000000, 30, NOW(), NOW(), 'E');

-- ============================
-- INIT LOBBY
-- ============================
INSERT INTO Lobby (id, name, lob_type_id, created_at, updated_at) VALUES
('YghjKl9N-1kjL-3kHl8-2jHg', 'Grand Ballroom', '1', NOW(), NOW()),
('2jkLmnO-3PqR-4sTuv-1wXyz', 'Skyline Terrace', '2', NOW(), NOW()),
('AbCdEf0-2GhI-3JkL-4MnOpQ', 'Ocean View Hall', '3', NOW(), NOW()),
('R5StUv6-WxYz-7XyZ-0aBcDe', 'Garden Pavilion', '4', NOW(), NOW()),
('FgHiJk1-LmNo-2PqRs-3TuVw', 'Royal Suite', '5', NOW(), NOW());

-- ============================
-- INIT FOODS
-- ============================
INSERT INTO Food (id, name, price, inventory, status, created_at, updated_at)
VALUES
('n1x2c3v4b5n6m7l8k9j0', 'Gỏi cuốn', 50000, 100, true, NOW(), NOW()),
('q1w2e3r4t5y6u7i8o9p0', 'Bánh mì thịt nướng', 30000, 150, true, NOW(), NOW()),
('a1s2d3f4g5h6j7k8l9z0', 'Phở bò', 45000, 200, true, NOW(), NOW());

-- ============================
-- INIT SERVICES
-- ============================
INSERT INTO Service (id, name, price, status, inventory, created_at, updated_at)
VALUES
('e4R5t6Y7u8I9o0P1q2w', 'Trang trí tiệc cưới', 20000000, true, 100, NOW(), NOW()),
('r4T5y6U7i8O9p0A1s2d', 'Quay phim, chụp ảnh', 15000000, true, 100, NOW(), NOW()),
('f6G7h8J9k0L1z2X3c4v', 'Nhóm nhạc, DJ', 12000000, true, 100, NOW(), NOW());
