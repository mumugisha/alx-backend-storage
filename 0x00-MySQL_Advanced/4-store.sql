--  Write a SQL script that creates a trigger that decreases the quantity of an item after adding a new order.
CREATE TRIGGER update_product_quantity_Number1
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items 
    SET quantity = quantity - NEW.order_quantity_1N 
    WHERE name = NEW.ordered_product_P;
