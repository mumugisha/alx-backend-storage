--  Write a SQL script that creates a trigger that decreases the quantity of an item after adding a new order.
CREATE TRIGGER decrease_item_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    -- Update the quantity of the item in the items table, allowing quantity to be negative
    UPDATE items 
    SET quantity = quantity - NEW.order_quantity
    WHERE name = NEW.ordered_product;
