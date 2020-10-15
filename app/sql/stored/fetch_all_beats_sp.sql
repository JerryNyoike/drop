DROP PROCEDURE IF EXISTS GetAllBeats; 

CREATE PROCEDURE GetAllBeats(IN fetch_limit INT)
BEGIN
	DECLARE beat_id VARCHAR(1000);
	DECLARE beat_name VARCHAR(50);
	DECLARE beat_file VARCHAR(100);
	DECLARE lease_price INT;
	DECLARE selling_price INT;
	DECLARE upload_date DATETIME;
	DECLARE producer_id VARCHAR(1000);
	DECLARE producer_name VARCHAR(50);
	DECLARE beat_categories VARCHAR(500);
	DECLARE finished INTEGER DEFAULT 0;

	DECLARE beats_cursor 
		CURSOR FOR 
			SELECT BIN_TO_UUID(beat.beat_id) beat_id, 
				beat.name, 
				beat.beat_file, 
				beat.lease_price, 
				beat.selling_price, 
				beat.upload_date,
				BIN_TO_UUID(producer.producer_id) producer_id, 
				producer.name producer 
			FROM 
				beat 
			INNER JOIN 
				producer 
			ON 
				beat.producer_id=producer.producer_id 
			LIMIT
				fetch_limit;

	DECLARE CONTINUE HANDLER 
    	FOR NOT FOUND SET finished = 1;

	OPEN beats_cursor;

	beats_loop: LOOP
		FETCH beats_cursor INTO 
			beat_id, 
			beat_name, 
			beat_file, 
			lease_price, 
			selling_price, 
			upload_date, 
			producer_id, 
			producer_name;

		IF finished = 1 THEN 
			LEAVE beats_loop;
		END IF;

		SET beat_categories = '';
	   	SELECT 
	   		CONCAT(category, ", ", beat_categories)
			FROM 
				beat_category 
		WHERE 
			beat_id = UUID_TO_BIN(beat_id);

		SELECT 
			beat_id, 
			beat_name, 
			beat_file, 
			lease_price, 
			selling_price, 
			upload_date, 
			producer_id, 
			producer_name, 
			beat_categories;

	END LOOP beats_loop;

	CLOSE beats_cursor;
END;