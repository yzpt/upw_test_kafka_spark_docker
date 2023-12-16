The `server.properties` file for Apache Kafka is typically located in the `config` directory within your Kafka installation directory. Here are the general steps to find it:

1. **Kafka Installation Directory:**
   Locate the directory where you have installed Apache Kafka. The exact path will depend on how you installed Kafka on your system.

2. **Navigate to the Config Directory:**
   Inside the Kafka installation directory, there should be a subdirectory named `config`. Navigate to this directory.

3. **Find `server.properties`:**
   Look for a file named `server.properties` within the `config` directory. This file contains the configuration settings for your Kafka broker.

If you cannot find the `server.properties` file in the `config` directory, you can check the Kafka broker startup script (`bin/kafka-server-start.sh` on Unix-like systems or `bin\windows\kafka-server-start.bat` on Windows) to see if it explicitly specifies a different configuration file using the `--override` option. The startup script might include a line like:

```bash
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/your-custom-server.properties
```

In this case, you should look for and edit the specified custom configuration file.

Remember to make backups of configuration files before making changes and restart the Kafka broker after modifying the `server.properties` file for changes to take effect.