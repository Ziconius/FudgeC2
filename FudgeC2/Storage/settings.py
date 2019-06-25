class Settings():
    # If the database does not exist it will be created in Storage/<name>.sql
    database_name = "____fudge.sql"
    # The port which FudgeC2 will run on. This will remove the port from available listener ports.
    server_app_port = 5001
    # For Flask implemented HTTPS set value to 'adhoc'. For HTTP set value to None
    server_app_ssl = None # 'adhoc'
    # This should be set to False for any non-development/testing deployments.
    server_app_debug = True

    # Cert & key file names used for TLS connections. These should be PEM formatted.
    #   Files will be stored in: '<install dir>/FudgeC2/Storage'. If these are set to
    #   None then HTTPS will not not be enabled.
    tls_listener_cert = "server.crt"
    tls_listener_key = "server.key"