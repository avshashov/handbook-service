INSERT INTO building (building_id, address, latitude, longitude)
VALUES (1, 'ул. Ленина, д. 1', 55.755826, 37.617300),
       (2, 'ул. Гоголя, д. 10', 55.740911, 37.594444);

INSERT INTO activity (activity_id, name, parent_id)
VALUES (1, 'Еда', NULL),
       (2, 'Мясная продукция', 1),
       (3, 'Молочная продукция', 1),
       (4, 'Автомобили', NULL),
       (5, 'Легковые', 4),
       (6, 'Грузовые', 4),
       (7, 'Запчасти', 5),
       (8, 'Аксессуары', 5);

INSERT INTO organization (organization_id, name, building_id)
VALUES (1, 'ООО Рога и Копыта', 1),
       (2, 'СыроДел', 1),
       (3, 'Автосервис Мотор', 2);

INSERT INTO organization_activity (organization_id, activity_id)
VALUES (1, 2),
       (1, 3),
       (2, 3),
       (3, 5);

INSERT INTO organization_phone (phone_id, number, organization_id)
VALUES (1, '+7 (495) 123-45-67', 1),
       (2, '+7 (495) 123-88-99', 1),
       (3, '+7 (499) 321-11-22', 2),
       (4, '+7 (495) 777-88-99', 3);
