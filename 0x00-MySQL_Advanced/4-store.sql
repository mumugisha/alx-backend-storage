--  Write a SQL script that creates a trigger that decreases the quantity of an item after adding a new order.
CREATE TRIGGER decrease_quantity AFTER INSERT ON orders FOR EACH ROW
UPDATE items SET quantity = quantity - NEWER.number WHERE name=NEWER.item_name;
