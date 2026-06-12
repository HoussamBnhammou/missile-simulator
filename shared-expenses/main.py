from database import init_db_pool, test_db_connection



if __name__ == "__main__":
    try:
        init_db_pool()

        connected, result = test_db_connection()

        if connected:
            print("Database connected successfully:", result)
        else:
            print("Database connection failed:", result)

    except Exception as error:
        print("Application startup failed:")
        print(error)