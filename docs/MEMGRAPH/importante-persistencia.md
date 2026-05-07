[Database management](https://memgraph.com/docs/database-management "Database management")Configuration

# Configuration

Memgraph has a set of configuration options that can be fine-tuned for specific needs.

The main Memgraph configuration file is available at the `/etc/memgraph/memgraph.conf`. The file contains a set of default configuration values and key-value pairs that can be modified to suit your specific needs.

Each configuration setting is in the form: `--setting-name=value`.

You can check the current configuration by using the following query:

```
SHOW CONFIG;
```

## Changing configuration[](https://memgraph.com/docs/database-management/configuration#changing-configuration)

The `memgraph.conf` file is the persistency for configuration. Changing the configuration settings depends on the way you are using Memgraph and the configuration settings you want to change.

Most of the configuration changes need to happen before Memgraph is started. Still, a set of configuration settings can be [changed during runtime](https://memgraph.com/docs/configuration/configuration-settings#change-configuration-settings-during-runtime).

Changing the configuration settings for Memgraph differs if you are using Memgraph with **Docker**, **Docker Compose**, or if it was installed on the native **Linux**.

### Pass the configuration flags

The most simple way to change the configuration with Docker is by passing the configuration options within the `docker run` command. For example, if you want to limit memory usage for the whole instance to 50 MiB and set the log level to `TRACE`, pass the configuration argument like this.

```
docker run -p 7687:7687 -p 7444:7444 memgraph/memgraph --memory-limit=50 --log-level=TRACE
```

### Update the configuration file

Another way of updating the default configuration is by updating the configuration file on the running instance, but such action requires restart so the update is applied. Here are the steps to change the default configuration file:

### Start Memgraph

Start Memgraph with a `docker run` command.

### Find container ID

Open a new terminal and find the `CONTAINER ID` of the Memgraph Docker container using the following command:

```
docker ps
```

### Enter the container

Enter the Docker container with the following command:

```
docker exec -it -u 0 <CONTAINER ID> bash
```

### Install the text editor of your choice

For example, if you want to use `vim` run:

```
apt-get update && apt-get install -y vim
```

### Edit the configuration file

The file is located at `/etc/memgraph/memgraph.conf`.

### Restart the instance

Run the following command:

```
docker restart <CONTAINER ID>
```

### Provide additional configuration file

To achieve a different configuration on startup, you can also provide the path to the additional configuration file which will override the default one. The file should contain the configuration settings in the form `--setting-name=value`. Still, if any configuration settings are set as arguments, they will override the settings in the additional configuration file as well. Providing the path to the additional configuration file requires more steps than setting the configuration via arguments. That’s because the file you’re pointing to must be located within the container before the container is running. To provide the additional configuration file, follow these steps:

### Create a container

Create a Docker container with the `--flag-file` argument pointing to the location where you’ll save the additional configuration file. The file must be saved within the container, ideally in the `/etc/memgraph` folder, where the default configuration file is stored.

```
docker create --name memgraph_container -p 7687:7687 -p 7444:7444 memgraph/memgraph --flag-file=/etc/memgraph/my.conf 
```

Besides the `--flag-file` flag, you can [set the environment variable](https://memgraph.com/docs/database-management/configuration#environment-variables) `MEMGRAPH_CONFIG` to achieve the same.

### Copy the additional configuration file

```
docker cp my.conf memgraph_container:/etc/memgraph/my.conf
```

### Start the container

```
docker start memgraph_container
```

---

### Change configuration during runtime[](https://memgraph.com/docs/database-management/configuration#change-configuration-during-runtime)

Memgraph contains settings that can be modified during runtime using a Cypher query. Some runtime settings are persisted between multiple runs, while others will fallback to the value of the command-line argument.

| Setting name               | Description                                                                                                                                                                                                                                                                            | Persistent between runs |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| organization.name          | Name of the organization using the instance of Memgraph (used for verifying the license key).                                                                                                                                                                                          | yes                     |
| enterprise.license         | License key for Memgraph Enterprise.                                                                                                                                                                                                                                                   | yes                     |
| server.name                | Bolt server name.                                                                                                                                                                                                                                                                      | yes                     |
| query.timeout              | Maximum allowed query execution time. Value of 0 means no limit.                                                                                                                                                                                                                       | yes                     |
| log.level                  | Minimum log level. Allowed values: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL.                                                                                                                                                                                                       | no                      |
| log.to_stderr              | Log messages go to `stderr` in addition to `logfiles`.                                                                                                                                                                                                                                 | no                      |
| cartesian-product-enabled  | Enforces cartesian product operator during query matching.                                                                                                                                                                                                                             | no                      |
| hops_limit_partial_results | If set to `true`, partial results are returned when the hops limit is reached. If set to `false`, an exception is thrown when the hops limit is reached. The default value is `true`.                                                                                                  | yes                     |
| timezone                   | IANA timezone identifier string setting the instance’s timezone.                                                                                                                                                                                                                       | yes                     |
| storage.snapshot.interval  | Define periodic snapshot schedule via 6-field cron expression (seconds, minute, hour, day of month, month, day of week—an [Enterprise feature](https://memgraph.com/docs/database-management/enabling-memgraph-enterprise)) or as a period in seconds. Set to empty string to disable. | no                      |
| storage-gc-aggressive      | Enables aggressive garbage collection, which performs full cleanup on GC call where deltas, vertices, edges or indices and constraints skip lists are being cleaned up. This setting requires taking a unique lock that will temporarily block the system during garbage collection.   | yes                     |
| storage.access_timeout_sec | Storage access timeout in seconds. Guards against queries waiting indefinitely for storage access. Valid range: [1, 1000000]. Corresponds to `--storage-access-timeout-sec`.                                                                                                           | no                      |
| aws.region                 | AWS region in which your S3 service is located.                                                                                                                                                                                                                                        | yes                     |
| aws.access_key             | Access key used to READ the file from S3.                                                                                                                                                                                                                                              | yes                     |
| aws.secret_key             | Secret key used to READ the file from S3.                                                                                                                                                                                                                                              | yes                     |
| aws.endpoint_url           | URL on which S3 can be accessed (if using some other S3-compatible storage).                                                                                                                                                                                                           | yes                     |

All settings can be fetched by calling the following query:

```
SHOW DATABASE SETTINGS;
```

To check the value of a single setting, you can use a slightly different query:

```
SHOW DATABASE SETTING "setting.name";
```

If you want to change a value for a specific setting, following query should be used:

```
SET DATABASE SETTING "setting.name" TO "some-value";
```

For reusable query values accessed as `$name`, see [Server-side parameters](https://memgraph.com/docs/database-management/server-side-parameters). Unlike database settings, server-side parameters are resolved during query execution.

### Multitenancy and configuration[](https://memgraph.com/docs/database-management/configuration#multitenancy-and-configuration)

If you are using a multi-tenant architecture, all isolated databases share identical configurations. At the moment, there is no way to specify a per-database configuration.

## List of configuration flags[](https://memgraph.com/docs/database-management/configuration#list-of-configuration-flags)

### Audit log[](https://memgraph.com/docs/database-management/configuration#audit-log)

This section contains the list of flags that are used to configure the audit logging.

| Flag                               | Description                                                                                  |
| ---------------------------------- | -------------------------------------------------------------------------------------------- |
| `--audit-enabled`                  | Enables audit logging.                                                                       |
| `--audit-buffer-size`              | Controls the in-memory buffer size used for audit logs.                                      |
| `--audit-buffer-flush-interval-ms` | Controls the time interval (in milliseconds) used for flushing the in-memory buffer to disk. |

### Auth module[](https://memgraph.com/docs/database-management/configuration#auth-module)

This section contains the list of flags that are used to configure the external auth module authentication and authorization mechanisms used by Memgraph.

| Flag                             | Description                                                                                                                                                                                                                                                                                                    |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--auth-module-mappings`         | Associates auth schemes to external modules. A mapping is structured as follows: `<scheme>:<absolute path to module>` and individual entries are separated with `;`. SSO schemes with default module paths can omit the path. If the mapping contains whitespace, enclose the flag value with quotation marks. |
| `--auth-module-executable`       | [DEPRECATED] Path to the executable that should be used for user authentication/authorization. Replaced by `--auth-module-mappings` from Memgraph 2.18.                                                                                                                                                        |
| `--auth-module-timeout-ms`       | Specifies the maximum time that Memgraph will wait for a response from the external auth module.                                                                                                                                                                                                               |
| `--auth-password-permit-null`    | Can be set to false to disable null passwords.                                                                                                                                                                                                                                                                 |
| `--auth-password-strength-regex` | The regular expression that should be used to match the entire entered password to ensure its strength. The syntax for regular expressions is derived from a [modified version of the ECMAScript regular expression grammar](https://en.cppreference.com/w/cpp/regex/ecmascript).                              |
| `--auth-user-or-role-regex`      | Set to the regular expression that each user or role name must fulfill. The syntax for regular expressions is derived from a [modified version of the ECMAScript regular expression grammar](https://en.cppreference.com/w/cpp/regex/ecmascript).                                                              |

### Bolt[](https://memgraph.com/docs/database-management/configuration#bolt)

This section contains the list of flags that are used to configure the Bolt protocol used by Memgraph.

| Flag                                                                                    | Description                                                                                                                     | Type       |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `--bolt-address=0.0.0.0`                                                                | IP address on which the Bolt server should listen.                                                                              | `[string]` |
| `--bolt-cert-file`                                                                      | Certificate file which should be used for the Bolt server.                                                                      | `[string]` |
| `--bolt-key-file`                                                                       | Key file which should be used for the Bolt server.                                                                              | `[string]` |
| `--bolt-num-workers`                                                                    | Number of workers used by the Bolt server.<br>By default, this will be the number of processing units available on the machine. | `[int32]`  |
| `--bolt-port=7687`                                                                      | Port on which the Bolt server should listen.                                                                                    | `[int32]`  |
| `--bolt-server-name-for-init=Neo4j/v5.11.0 compatible graph database server - Memgraph` | Server name which the database should send to the client in the Bolt INIT message.                                              | `[string]` |

Memgraph does not limit the maximum amount of simultaneous sessions. Transactions within all open sessions are served with a limited number of Bolt workers simultaneously.

### High availability[](https://memgraph.com/docs/database-management/configuration#high-availability)

This section contains the list of flags that are used to configure highly available cluster in Memgraph.

| Flag                                      | Description                                                                                                                                                  | Type       |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------- |
| `--coordinator-id`                        | Raft server id on coordinator instance.                                                                                                                      | `[int32]`  |
| `--coordinator-port`                      | Raft server’s port on coordinator instance.                                                                                                                  | `[uint32]` |
| `--management-port`                       | Port on which replication instances receive messages from coordinator .                                                                                      | `[uint32]` |
| `--instance-health-check-frequency-sec=1` | The interval between two health checks that coordinator does on replication instances.                                                                       | `[uint32]` |
| `—instance-down-timeout-sec=5             | Number of seconds that need to pass before replication instance is considered down. Must be greater or equal to the `--instance-health-check-frequency-sec`. | `[uint32]` |
| `--nuraft-log-file`                       | Path to the file where NuRaft logs are saved.                                                                                                                | `[string]` |
| `--coordinator-hostname`                  | Coordinator’s instance hostname. Used only in `SHOW INSTANCES` query.                                                                                        | `[string]` |

### Query[](https://memgraph.com/docs/database-management/configuration#query)

This section contains the list of flags that are used to configure query execution in Memgraph.

| Flag                                                                            | Description                                                                                                                                                                                                      | Type       |
| ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `--cartesian-product-enabled=true`                                              | Enforces whether cartesian product matching is going to be used in the plans.                                                                                                                                    | `[bool]`   |
| `--query-callable-mappings-path=/etc/memgraph/apoc_compatibility_mappings.json` | Path to the JSON file that contains possible alias mappings for query procedures in the form of key-value pairs.                                                                                                 | `[string]` |
| `--query-cost-planner=true`                                                     | Use the cost-estimating query planner. When enabled (`true`), Memgraph generates multiple query plans, selecting the one with the lowest cost. If disabled (`false`), it creates a single plan that is executed. | `[bool]`   |
| `--query-execution-timeout-sec=600`                                             | Maximum allowed query execution time.<br>Queries exceeding this limit will be aborted. Value of 0 means no limit.                                                                                                | `[uint64]` |
| `--query-max-plans=1000`                                                        | Maximum number of generated plans for a query.                                                                                                                                                                   | `[uint64]` |
| `--query-modules-directory=/usr/lib/memgraph/query_modules`                     | Directory where modules with custom query procedures are stored. NOTE: Multiple comma-separated directories can be defined.                                                                                      | `[string]` |
| `--query-plan-cache-max-size=1000`                                              | Maximum number of query plans to cache.                                                                                                                                                                          | `[int32]`  |
| `--query-vertex-count-to-expand-existing=10`                                    | Maximum count of indexed vertices which provoke indexed lookup and then expand to existing,<br>instead of a regular expand. Default is 10, to turn off use -1.                                                   | `[int64]`  |
| `--query-log-directory=/var/log/memgraph/session_trace`                         | Location to store log files for session tracing.                                                                                                                                                                 | `[string]` |

### Storage[](https://memgraph.com/docs/database-management/configuration#storage)

This section contains the list of flags that are used to configure storage usage in Memgraph.

| Flag                                                         | Description                                                                                                                                                                                                                                           | Type       |
| ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `--storage-delta-on-identical-property-update=true`          | Controls whether a delta object will be created if a property is updated with the same value.                                                                                                                                                         | `[bool]`   |
| `--storage-gc-cycle-sec=30`                                  | Storage garbage collector interval (in seconds).                                                                                                                                                                                                      | `[uint64]` |
| `--storage-python-gc-cycle-sec=180`                          | Interval for manual complete garbage collection in Python (in seconds).                                                                                                                                                                               | `[uint64]` |
| `--storage-items-per-batch=1000000`                          | The number of edges and vertices stored in a batch in a snapshot file.                                                                                                                                                                                | `[uint64]` |
| `--storage-parallel-schema-recovery=false`                   | Controls whether the indices and constraints creation can be done in a multithreaded fashion during recovery.                                                                                                                                         | `[bool]`   |
| `--storage-properties-on-edges=true`                         | Controls whether edges have properties.                                                                                                                                                                                                               | `[bool]`   |
| `--storage-recovery-thread-count`                            | The number of threads used to recover persisted data from disk. Defaults to using system’s maximum thread count.                                                                                                                                      | `[uint64]` |
| `--storage-snapshot-interval-sec=300`                        | Storage snapshot creation interval (in seconds). Set to 0 to disable periodic snapshot creation.                                                                                                                                                      | `[uint64]` |
| `--storage-snapshot-interval="300`”                          | Define periodic snapshot schedule via 6-field cron expression (with seconds) or as a period in seconds. Set to empty string to disable.                                                                                                               | `[string]` |
| `--storage-snapshot-on-exit=true`                            | Controls whether the storage creates another snapshot on exit.                                                                                                                                                                                        | `[bool]`   |
| `--storage-snapshot-retention-count=3`                       | The number of snapshots that should always be kept.                                                                                                                                                                                                   | `[uint64]` |
| `--storage-parallel-snapshot-creation=false`                 | Controls whether the snapshot creation can be done in a multi-threaded fashion.                                                                                                                                                                       | `[bool]`   |
| `--storage-snapshot-thread-count`                            | The number of threads used to create snapshots. Defaults to using system’s maximum thread count.                                                                                                                                                      | `[uint64]` |
| `--storage-wal-enabled=true`                                 | Controls whether the storage uses write-ahead-logging. To enable WAL, periodic snapshots must be enabled.                                                                                                                                             | `[bool]`   |
| `--storage-wal-file-flush-every-n-tx=100000`                 | Issue a ‘fsync’ call after this amount of transactions are written to the WAL file. Set to 1 for fully synchronous operation.                                                                                                                         | `[uint64]` |
| `--storage-wal-file-size-kib=20480`                          | Minimum file size of each WAL file.                                                                                                                                                                                                                   | `[uint64]` |
| `--storage-mode=IN_MEMORY_TRANSACTIONAL`                     | The storage mode Memgraph will run on startup. Can be IN_MEMORY_TRANSACTIONAL, IN_MEMORY_ANALYTICAL or ON_DISK_TRANSACTIONAL.                                                                                                                         | `[string]` |
| `--storage-enable-schema-metadata=false`                     | Facilitates the utilization of a specialized cache designed to store specific metadata related to the database.                                                                                                                                       | `[bool]`   |
| `--storage-enable-edges-metadata=false`                      | Utilizes additional memory to store metadata related to edges. This metadata is used to speed up id based lookups on edges.                                                                                                                           | `[bool]`   |
| `--storage-automatic-label-index-creation-enabled=false`     | Enables automatic creation of indices on labels. Only usable in IN_MEMORY_TRANSACTIONAL mode.                                                                                                                                                         | `[bool]`   |
| `--storage-automatic-edge-type-index-creation-enabled=false` | Enables automatic creation of indices on edge types. Only usable in IN_MEMORY_TRANSACTIONAL mode.                                                                                                                                                     | `[bool]`   |
| `--storage-property-store-compression-enabled=false`         | Controls whether the properties should be compressed in the storage.                                                                                                                                                                                  | `[bool]`   |
| `--storage-property-store-compression-level=mid`             | Controls property store compression level. Allowed values: low, mid, high                                                                                                                                                                             | `[string]` |
| `--storage-floating-point-resolution-bits=64`                | Max bits for floating-point property storage. Allowed values: 16, 32, 64. Lower values save memory but reduce precision.                                                                                                                              | `[uint64]` |
| `--storage-access-timeout-sec=1`                             | Storage access timeout in seconds. Used to fine-tune the responsiveness and guard against queries indefinitely waiting. Can also be changed at runtime via `SET DATABASE SETTING 'storage.access_timeout_sec' TO 'value'`. Valid range: [1, 1000000]. | `[uint64]` |
| `--storage-enable-backup-dir=true`                           | Controls whether `.old` directory will be used to store backup.                                                                                                                                                                                       | `[bool]`   |

### Streams[](https://memgraph.com/docs/database-management/configuration#streams)

This section contains the list of flags that are used to configure stream connections in Memgraph.

| Flag                                       | Description                                                                                                 | Type       |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------- | ---------- |
| `--kafka-bootstrap-servers`                | List of Kafka brokers as a comma separated list of broker `host` or `host:port`.                            | `[string]` |
| `--pulsar-service-url`                     | The service URL that will allow Memgraph to locate the Pulsar cluster.                                      | `[string]` |
| `--stream-transaction-conflict-retries=30` | Number of times to retry a conflicting transaction of a stream.                                             | `[uint32]` |
| `--stream-transaction-retry-interval=500`  | The interval to wait (measured in milliseconds) before retrying to execute again a conflicting transaction. | `[uint32]` |

### AWS[](https://memgraph.com/docs/database-management/configuration#aws)

This section contains the list of flags that are used when connecting to S3-compatible storage.

| Flag                 | Description                                                                  | Type       |
| -------------------- | ---------------------------------------------------------------------------- | ---------- |
| `--aws-region`       | AWS region in which your S3 service is located.                              | `[string]` |
| `--aws-access-key`   | Access key used to READ the file from S3.                                    | `[string]` |
| `--aws-secret-key`   | Secret key used to READ the file from S3.                                    | `[string]` |
| `--aws-endpoint-url` | URL on which S3 can be accessed (if using some other S3-compatible storage). | `[string]` |

### Other[](https://memgraph.com/docs/database-management/configuration#other)

This section contains the list of all other relevant flags used within Memgraph.

| Flag                                          | Description                                                                                                                                                                                                                                                                                                                                                 | Type       |
| --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `--allow-load-csv=true`                       | Controls whether LOAD CSV clause is allowed in queries.                                                                                                                                                                                                                                                                                                     | `[bool]`   |
| `--also-log-to-stderr=false`                  | Log messages go to stderr in addition to logfiles.                                                                                                                                                                                                                                                                                                          | `[bool]`   |
| `--data-directory=/var/lib/memgraph`          | Path to directory in which to save all permanent data.                                                                                                                                                                                                                                                                                                      | `[string]` |
| `--data-recovery-on-startup=true`             | Facilitates recovery of one or more individual databases and their contents during startup. Replaces `--storage-recover-on-startup`                                                                                                                                                                                                                         | `[bool]`   |
| `--debug-query-plans=false`                   | Enable DEBUG logging of potential query plans.                                                                                                                                                                                                                                                                                                              | `[string]` |
| `--delta-chain-cache-threshold=128`           | The minimum number of deltas worth caching when rebuilding a certain object’s state. Useful when executing parallel transactions dependent on changes of a frequently changed graph object, to lower CPU usage. Must be a positive non-zero integer.                                                                                                        | `[uint64]` |
| `--file-download-conn-timeout-sec`            | The timeout for establishing a connection to the remote server when downloading a file.                                                                                                                                                                                                                                                                     | `[uint64]` |
| `--flag-file`                                 | Path to the additional configuration file, overrides the default configuration settings.                                                                                                                                                                                                                                                                    | `[string]` |
| `--help`                                      | Show help on all flags and exit. The default values is `false`.                                                                                                                                                                                                                                                                                             | `[bool]`   |
| `--help-xml`                                  | Produce an XML version of help and exit. The default values is `false`.                                                                                                                                                                                                                                                                                     | `[bool]`   |
| `--init-file`                                 | Path to the CYPHERL file which contains queries that need to be executed before the Bolt server starts, such as creating users.                                                                                                                                                                                                                             | `[string]` |
| `--init-data-file`                            | Path to the CYPHERL file, which contains queries that need to be executed after the Bolt server starts.                                                                                                                                                                                                                                                     | `[string]` |
| `--isolation-level=SNAPSHOT_ISOLATION`        | Isolation level used for the transactions. Allowed values: SNAPSHOT_ISOLATION, READ_COMMITTED, READ_UNCOMMITTED.                                                                                                                                                                                                                                            | `[string]` |
| `--log-file=/var/log/memgraph/memgraph.log`   | Path to where the log should be stored. If set to an empty string (`--log-file=`), no logs will be saved.                                                                                                                                                                                                                                                   | `[string]` |
| `--log-level=WARNING`                         | Minimum log level. Allowed values: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL.                                                                                                                                                                                                                                                                            | `[string]` |
| `--logger-type=sync`                          | Type of logger used by Memgraph. Allowed values: `sync`, `async`. When set to `async`, log messages are buffered and written in a background thread, reducing the performance impact of logging on query execution.                                                                                                                                         | `[string]` |
| `--log-retention-days=35`                     | Controls for how many days daily log files will be preserved. Allowed values: 1–1000000.                                                                                                                                                                                                                                                                    | `[uint64]` |
| `--memory-limit=0`                            | Total memory limit in MiB. Set to 0 to use the default values which are 100% of the physical memory if the swap is enabled and 90% of the physical memory otherwise.                                                                                                                                                                                        | `[uint64]` |
| `--metrics-address`                           | Host for HTTP server for exposing metrics.                                                                                                                                                                                                                                                                                                                  | `[string]` |
| `--metrics-port`                              | Port for HTTP server for exposing metrics.                                                                                                                                                                                                                                                                                                                  | `[uint64]` |
| `--memory-warning-threshold=1024`             | Memory warning threshold, in MB. If Memgraph detects there is less available RAM it will log a warning.<br>Set to 0 to disable.                                                                                                                                                                                                                             | `[uint64]` |
| `--monitoring-address="0.0.0.0"`              | IP address where the Memgraph’s monitoring WebSocket server should listen.                                                                                                                                                                                                                                                                                  | `[string]` |
| `--monitoring-port=7444`                      | Port on which the Memgraph’s monitoring WebSocket server should listen.                                                                                                                                                                                                                                                                                     | `[int32]`  |
| `--password-encryption-algorithm=bcrypt`      | Algorithm used for password encryption. Defaults to BCrypt. Allowed values: `bcrypt`, `sha256`, `sha256-multiple` (SHA256 with multiple iterations)                                                                                                                                                                                                         | `[string]` |
| `--replication-replica-check-frequency-sec`   | The time duration in seconds between two replica checks/pings. If < 1, replicas will not be checked at all and the replica will never be recovered. The MAIN instance allocates a new thread for each REPLICA.                                                                                                                                              | `[uint64]` |
| `--replication-restore-state-on-startup=true` | Set to `true` when initializing an instance to restore the replication role and configuration upon restart.                                                                                                                                                                                                                                                 | `[bool]`   |
| `--schema-info-enabled=false`                 | Set to `true` to enable run-time schema info tracking.                                                                                                                                                                                                                                                                                                      | `[bool]`   |
| `--telemetry-enabled=true`                    | Set to true to enable telemetry. We collect information about the running system (CPU and memory information), information about the database runtime (vertex and edge counts and resource usage), and aggregated statistics about some features of the database (e.g. how many times a feature is used) to allow for an easier improvement of the product. | `[bool]`   |

### Environment variables[](https://memgraph.com/docs/database-management/configuration#environment-variables)

This section contains the list of environment variables that can be used to configure Memgraph.

Before the running of Memgraph, you can set the following environment variables:

| Variable                         | Description                                                                                                                                                                                                                                        | Type       |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| MEMGRAPH_USER                    | Specifies the username for connecting to Memgraph. If the user does not exist, a new one is created with this username. Manual entry of credentials is always necessary when accessing Memgraph using Memgraph Lab.                                | `[string]` |
| MEMGRAPH_PASSWORD                | Specifies the password for the user. If creating a new user, this password is assigned. For existing users, this setting does not change the password. Manual entry of credentials is always necessary when accessing Memgraph using Memgraph Lab. | `[string]` |
| MEMGRAPH_PASSFILE                | Path to the file that contains the username and password for creating a user. Data in the file should be in the format `username:password`. If your username or password contains `:`, add `\` before it, for example, `us\:ername:password`.      | `[string]` |
| MEMGRAPH_CONFIG                  | Path to the additional configuration file.                                                                                                                                                                                                         | `[string]` |
| MEMGRAPH_MANAGEMENT_PORT         | Port on which data instance management servers or the coordinator management server will be started.                                                                                                                                               | `[int]`    |
| MEMGRAPH_COORDINATOR_PORT        | Port on which Raft servers will be started.                                                                                                                                                                                                        | `[int]`    |
| MEMGRAPH_COORDINATOR_ID          | Unique ID of the Raft server.                                                                                                                                                                                                                      | `[int]`    |
| MEMGRAPH_NURAFT_LOG_FILE         | Path to the file where NuRaft logs are saved.                                                                                                                                                                                                      | `[string]` |
| MEMGRAPH_COORDINATOR_HOSTNAME    | Instance’s hostname. Used as output of the `SHOW INSTANCES` query.                                                                                                                                                                                 | `[string]` |
| MEMGRAPH_HA_CLUSTER_INIT_QUERIES | Path to the file with queries to initialize the HA cluster.                                                                                                                                                                                        | `[string]` |
| MEMGRAPH_BOLT_PORT               | Bolt port used for Bolt server.                                                                                                                                                                                                                    | `[int]`    |
| MEMGRAPH_EXPERIMENTAL_ENABLED    | List of experimental features which the user wants to use.                                                                                                                                                                                         | `[string]` |
| MEMGRAPH_ENTERPRISE_LICENSE      | Memgraph enterprise license key.                                                                                                                                                                                                                   | `[string]` |
| MEMGRAPH_ORGANIZATION_NAME       | Organization name to which Memgraph license key was issued.                                                                                                                                                                                        | `[string]` |

In order to apply the environment variables with Memgraph, you can follow the steps below:

To set the environment variable when running Memgraph with Docker, use the following syntax:

```
docker run -p 7687:7687 -p 7444:7444 -e MEMGRAPH_USER=newUser -e MEMGRAPH_PASSWORD=pass memgraph/memgraph 
```

The above command will start Memgraph in Docker container and create a user with username `newUser` and password `pass`.

## Use `init` flags with Docker[](https://memgraph.com/docs/database-management/configuration#use-init-flags-with-docker)

With `init-file` and `init-data-file` configuration flags, you can execute queries from a CYPHERL file that need to be executed before or immediately after the Bolt server starts. The CYPHERL file the `init-file` flag points to is usually used to create users and set their passwords allowing only authorized users to access the data in the first run. The CYPHERL file the `init-data-file` points to is usually used to populate the database.

If you will run Memgraph with Docker, make sure that the `init-file` and `init-data-file` configuration flags are referring to the files inside the container before Memgraph starts. Files can’t be directly copied into a container before it’s started because the filesystem of the container doesn’t exist until it’s actually running. However, you can tackle this by using a Dockerfile.

In this guide you will learn how to:

- [**Use the `init-file` flag with Docker**](https://memgraph.com/docs/database-management/configuration#use-the-init-file-flag-with-docker)
- [**Use the `init-data-file` flag with Docker**](https://memgraph.com/docs/database-management/configuration#use-the-init-data-file-flag-with-docker)

If an exception occurs during the execution of init script the queries will continue with execution.

### Use the `init-file` flag with Docker[](https://memgraph.com/docs/database-management/configuration#use-the-init-file-flag-with-docker)

### Create all necessary files

First, create a local directory called `my_init_test` with `auth.cypherl` and Dockerfile inside it.

Below is the content of the `auth.cypherl` file:

```
CREATE USER memgraph1 IDENTIFIED BY '1234';
```

The Dockerfile should be defined like this:

```
FROM memgraph/memgraph:latest USER root COPY auth.cypherl /usr/lib/memgraph/auth.cypherl USER memgraph
```

The above Dockerfile builds an image based on `memgraph/memgraph:latest` image. For other images, [check Memgraph’s Docker Hub](https://hub.docker.com/u/memgraph). Then, it switches to the user `root` to be able to copy the local file to the container where Memgraph will be run. Due to the permissions set, it is recommended to copy it to `/usr/lib/memgraph/` or any subfolder within that folder. In the end, the user is switched back to `memgraph`.

### Build the Docker image

Open the terminal, place yourself in the `my_init_test` directory and build the image called `my_image` with the following command:

```
docker build -t my_image .
```

### Run the Docker image

Once you’ve built the Docker image, you can run it with the `init-file` flag set to the appropriate value:

```
docker run -it -p 7687:7687 -p 7444:7444 my_image --init-file=/usr/lib/memgraph/auth.cypherl
```

To check all available flags in Memgraph, refer to [the configuration reference guide](https://memgraph.com/docs/database-management/configuration).

### Connect to Memgraph

To verify that everything is set up correctly, [run Memgraph Lab](https://memgraph.com/docs/data-visualization) and connect to Memgraph. You’ll notice that you have to connect manually and input the correct username and password. This happened because `auth.cypherl` file was run before the Bolt server started. You can also run the `SHOW CONFIG` query:

![](https://memgraph.com/docs/_next/image?url=%2Fdocs%2F_next%2Fstatic%2Fmedia%2Fmemgraph-lab-init-file.3cc52c2e.png&w=3840&q=75)

Notice how the current value of `init_file` is updated with the path to the CYPHERL file inside the container.

### Use the `init-data-file` flag with Docker[](https://memgraph.com/docs/database-management/configuration#use-the-init-data-file-flag-with-docker)

### Create all necessary files

First, create a local directory called `my_init_test` with `data.cypherl` and Dockerfile inside it.

Below is the content of the `data.cypherl` file:

```
CREATE INDEX ON :__mg_vertex__(__mg_id__);CREATE (:__mg_vertex__:`Person` {__mg_id__: 0, `name`: "Peter"});CREATE (:__mg_vertex__:`Team` {__mg_id__: 1, `name`: "Engineering"});CREATE (:__mg_vertex__:`Repository` {__mg_id__: 2, `name`: "Memgraph"});CREATE (:__mg_vertex__:`Repository` {__mg_id__: 3, `name`: "MAGE"});CREATE (:__mg_vertex__:`Repository` {__mg_id__: 4, `name`: "GQLAlchemy"});CREATE (:__mg_vertex__:`Company` {__mg_id__: 5, `name`: "Memgraph"});CREATE (:__mg_vertex__:`File` {__mg_id__: 6, `name`: "welcome_to_engineering.txt"});CREATE (:__mg_vertex__:`Storage` {__mg_id__: 7, `name`: "Google Drive"});CREATE (:__mg_vertex__:`Storage` {__mg_id__: 8, `name`: "Notion"});CREATE (:__mg_vertex__:`File` {__mg_id__: 9, `name`: "welcome_to_memgraph.txt"});CREATE (:__mg_vertex__:`Person` {__mg_id__: 10, `name`: "Carl"});CREATE (:__mg_vertex__:`Folder` {__mg_id__: 11, `name`: "engineering_folder"});CREATE (:__mg_vertex__:`Person` {__mg_id__: 12, `name`: "Anna"});CREATE (:__mg_vertex__:`Folder` {__mg_id__: 13, `name`: "operations_folder"});CREATE (:__mg_vertex__:`Team` {__mg_id__: 14, `name`: "Operations"});CREATE (:__mg_vertex__:`File` {__mg_id__: 15, `name`: "operations101.txt"});CREATE (:__mg_vertex__:`File` {__mg_id__: 16, `name`: "expenses2022.csv"});CREATE (:__mg_vertex__:`File` {__mg_id__: 17, `name`: "salaries2022.csv"});CREATE (:__mg_vertex__:`File` {__mg_id__: 18, `name`: "engineering101.txt"});CREATE (:__mg_vertex__:`File` {__mg_id__: 19, `name`: "working_with_github.txt"});CREATE (:__mg_vertex__:`File` {__mg_id__: 20, `name`: "working_with_notion.txt"});CREATE (:__mg_vertex__:`Team` {__mg_id__: 21, `name`: "Marketing"});CREATE (:__mg_vertex__:`Person` {__mg_id__: 22, `name`: "Julie"});CREATE (:__mg_vertex__:`Account` {__mg_id__: 23, `name`: "Facebook"});CREATE (:__mg_vertex__:`Account` {__mg_id__: 24, `name`: "LinkedIn"});CREATE (:__mg_vertex__:`Account` {__mg_id__: 25, `name`: "HackerNews"});CREATE (:__mg_vertex__:`File` {__mg_id__: 26, `name`: "welcome_to_marketing.txt"});MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 0 AND v.__mg_id__ = 1 CREATE (u)-[:`IS_PART_OF`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 0 AND v.__mg_id__ = 5 CREATE (u)-[:`IS_PART_OF`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 0 AND v.__mg_id__ = 9 CREATE (u)-[:`HAS_ACCESS_TO`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 0 AND v.__mg_id__ = 14 CREATE (u)-[:`IS_PART_OF`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 1 AND v.__mg_id__ = 2 CREATE (u)-[:`HAS_ACCESS_TO`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 1 AND v.__mg_id__ = 3 CREATE (u)-[:`HAS_ACCESS_TO`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 1 AND v.__mg_id__ = 4 CREATE (u)-[:`HAS_ACCESS_TO`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 1 AND v.__mg_id__ = 6 CREATE (u)-[:`HAS_ACCESS_TO`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 1 AND v.__mg_id__ = 11 CREATE (u)-[:`HAS_ACCESS_TO`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 5 AND v.__mg_id__ = 1 CREATE (u)-[:`HAS_TEAM`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 5 AND v.__mg_id__ = 21 CREATE (u)-[:`HAS_TEAM`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 5 AND v.__mg_id__ = 14 CREATE (u)-[:`HAS_TEAM`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 6 AND v.__mg_id__ = 7 CREATE (u)-[:`IS_STORED_IN`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 6 AND v.__mg_id__ = 8 CREATE (u)-[:`IS_STORED_IN`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 9 AND v.__mg_id__ = 12 CREATE (u)-[:`CREATED_BY`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 10 AND v.__mg_id__ = 1 CREATE (u)-[:`IS_PART_OF`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 10 AND v.__mg_id__ = 5 CREATE (u)-[:`IS_PART_OF`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 10 AND v.__mg_id__ = 9 CREATE (u)-[:`HAS_ACCESS_TO`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 11 AND v.__mg_id__ = 7 CREATE (u)-[:`IS_STORED_IN`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 11 AND v.__mg_id__ = 18 CREATE (u)-[:`HAS_ACCESS_TO`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 11 AND v.__mg_id__ = 19 CREATE (u)-[:`HAS_ACCESS_TO`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 11 AND v.__mg_id__ = 20 CREATE (u)-[:`HAS_ACCESS_TO`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 12 AND v.__mg_id__ = 14 CREATE (u)-[:`IS_PART_OF`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 13 AND v.__mg_id__ = 15 CREATE (u)-[:`HAS_ACCESS_TO`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 13 AND v.__mg_id__ = 16 CREATE (u)-[:`HAS_ACCESS_TO`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 13 AND v.__mg_id__ = 17 CREATE (u)-[:`HAS_ACCESS_TO`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 13 AND v.__mg_id__ = 7 CREATE (u)-[:`IS_STORED_IN`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 14 AND v.__mg_id__ = 13 CREATE (u)-[:`HAS_ACCESS_TO`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 21 AND v.__mg_id__ = 23 CREATE (u)-[:`HAS_ACCESS_TO`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 21 AND v.__mg_id__ = 24 CREATE (u)-[:`HAS_ACCESS_TO`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 21 AND v.__mg_id__ = 25 CREATE (u)-[:`HAS_ACCESS_TO`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 21 AND v.__mg_id__ = 26 CREATE (u)-[:`HAS_ACCESS_TO`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 22 AND v.__mg_id__ = 21 CREATE (u)-[:`IS_PART_OF`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 22 AND v.__mg_id__ = 5 CREATE (u)-[:`IS_PART_OF`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 22 AND v.__mg_id__ = 9 CREATE (u)-[:`HAS_ACCESS_TO`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 26 AND v.__mg_id__ = 7 CREATE (u)-[:`IS_STORED_IN`]->(v);MATCH (u:__mg_vertex__), (v:__mg_vertex__) WHERE u.__mg_id__ = 26 AND v.__mg_id__ = 8 CREATE (u)-[:`IS_STORED_IN`]->(v);DROP INDEX ON :__mg_vertex__(__mg_id__);MATCH (u) REMOVE u:__mg_vertex__, u.__mg_id__;
```

These Cypher queries will create the *Identity and access management* dataset available in Memgraph Lab. You can get this CYPHERL file by exporting the dataset from the Memgraph Lab.

The Dockerfile should be defined like this:

```
FROM memgraph/memgraph:latest USER root COPY data.cypherl /usr/lib/memgraph/data.cypherl USER memgraph
```

The above Dockerfile builds an image based on `memgraph/memgraph:latest` image. For other images, [check Memgraph’s Docker Hub](https://hub.docker.com/u/memgraph). Then, it switches to the user `root` to be able to copy the local file to the container where Memgraph will be run. Due to the permissions set, it is recommended to copy it to `/usr/lib/memgraph/` or any subfolder within that folder. In the end, the user is switched back to `memgraph`.

### Build the Docker image

Open the terminal, place yourself in the `my_init_test` directory and build the image called `my_image` with the following command:

```
docker build -t my_image .
```

### Run the Docker image

Once you’ve built the Docker image, you can run it with the `init-data-file` flag set to the appropriate value:

```
docker run -it -p 7687:7687 -p 7444:7444 my_image --init-data-file=/usr/lib/memgraph/data.cypherl
```

### Connect to Memgraph

To verify that everything is set up correctly, [run Memgraph Lab](https://memgraph.com/docs/data-visualization), connect to Memgraph, and run the `SHOW CONFIG` query:

![](https://memgraph.com/docs/_next/image?url=%2Fdocs%2F_next%2Fstatic%2Fmedia%2Fmemgraph-lab-init-data-file.54b7b5ca.png&w=3840&q=75)

Notice how the database is already populated and the current value of `init_data_file` is updated with the path to the CYPHERL file inside the container.



# Memgraph Storage Modes Explained

By Katarina Supe

8 min readApril 11, 2024

Memgraph is an in-memory graph database that ensures data persistence through ACID compliance by default. While it uses snapshots and write-ahead logs (WAL) for data recovery, in some cases, such additional files and insurance are not necessary. Other databases and analytics tools offer snapshots or WAL, but Memgraph offers both with different storage modes.

Before you start using them, here's a helpful guide on Memgraph storage modes so you can understand when to use them and why.

## ACID Compliance in In-Memory Transactional Storage Mode

Previously, Memgraph only had one storage mode—[in-memory transactional](https://memgraph.com/docs/fundamentals/storage-memory-usage#in-memory-transactional-storage-mode-default). The idea was to achieve excellent performance with the in-memory storage but still be ACID compliant.

Under the hood, a Delta object is the primary tool with which Memgraph provides atomicity, consistency, isolation and durability. These objects, inspired by the research presented in the [Fast Serializable Multiversion Concurrency Control for Main-Memory Database Systems](https://db.in.tum.de/~muehlbau/papers/mvcc.pdf) paper, record all transaction modifications to nodes or relationships. This mechanism ensures that periodic snapshots and write-ahead logs (WAL) are accurately maintained on disk for durability purposes. By default, Memgraph retains the three most recent snapshots and WAL files in the /var/lib/memgraph directory, facilitating efficient [backup and recovery](https://memgraph.com/docs/configuration/data-durability-and-backup) processes.

Another transaction property is [isolation](https://memgraph.com/docs/fundamentals/transactions#isolation-levels). It determines how transaction integrity is visible to other users and systems. Isolation can have different levels. For example, a lower isolation level allows many users to access the same data simultaneously but increases the number of concurrency effects (such as dirty reads or lost updates). A higher isolation level secures data consistency but requires more system resources, increasing the chances that one transaction will block another.

Memgraph defaults to the `SNAPSHOT_ISOLATION` level. It guarantees that all transaction reads observe a consistent database snapshot. This level also mandates that concurrent transactions can’t successfully commit if they are updating the same graph object, and such execution leads to [conflicting transactions error](https://memgraph.com/docs/help-center/errors/transactions#conflicting-transactions).

You should either avoid such errors or retry the transaction for which its execution raised such an error. Still, it is essential to understand that those errors are expected to occur with concurrent transactions to ensure the ACID properties of the database transactions.

Because of strongly consistent ACID transactions in the in-memory transactional mode, you don’t have to worry about consistency even if you have mixed read and write transactions. Still, if you’re dealing with large-scale data import, you might notice memory overhead because Delta objects are quickly accumulated.

To avoid such issues and experience fast import without wasting valuable memory resources, Memgraph introduced the in-memory analytical storage mode.

## Fast Writes Without Memory Overhead: In-Memory Analytical Storage Mode

In the [in-memory analytical storage mode](https://memgraph.com/docs/fundamentals/storage-memory-usage#in-memory-analytical-storage-mode), Delta objects are disabled to achieve better performance without memory overhead. Which is significantly noticeable during data import. Besides that, no isolation levels are defined in the in-memory analytical storage mode.

Before diving into the details of this storage mode, let’s first explain the motivation behind disabling Delta objects. A while ago, we noticed a common challenge among our users: data import complexities. Since data import is one of the first steps when using a database, we knew we had to make improvements.

During data import, graph objects are frequently created and updated, which causes a fast accumulation of Delta objects. These objects, while crucial for maintaining ACID properties, also consume considerable memory resources. This is particularly noticeable when new relationships are formed, creating Deltas for both the starting and ending nodes. Although Deltas make it possible to undo such changes, they significantly slow down subsequent node updates, as every Delta must be processed before any new modification.

After detecting Delta objects as the main culprit for slow import, we were curious to know what would happen if we disabled them.

Here is the impact of removing Delta objects:

- Multiple transactions can modify the same object and create relationships on the same node concurrently (there are no concurrent transactions errors anymore)

- It leads to improved performance write-heavy workloads

- The trade-offs include a lack of ACID guarantees; though it’s possible to manually create snapshots for durability.

- Replication is disabled, as Deltas are essential for this process.

Everyone loves to hear about the positive impact on speed and performance, but let’s explain what not having ACID guarantees means.

- Deltas being disabled lead to no WALs being created, meaning that if a write transaction fails for any reason, the changes can’t be rolled back -> no **A**tomicity guarantees

- Transactions may fail and leave the database in an inconsistent state -> no **C**onsistency guarantees

- No isolation level, meaning if you have a long-running write transaction, other transactions can see the changes of ongoing transactions even if changes are not committed -> no **I**solation guarantees

- Snapshots and WALs are not created -> No **D**urability guarantees

When you understand what we’ve just covered and review the [implications](https://memgraph.com/docs/fundamentals/storage-memory-usage#implications), you can get the most out of this storage mode and achieve the best performance with low memory cost.

## Managing Large Datasets: Introducing On-Disk Transactional Storage Mode

What to do when the dataset is larger than the available RAM?

Ideally, if your data is larger than the available RAM, you would have a part of it stored on disk and the part used for the analysis in memory. Memgraph offers a third storage mode that does precisely that - [on-disk transactional storage mode](https://memgraph.com/docs/fundamentals/storage-memory-usage#on-disk-transactional-storage-mode).

Let's go over how Memgraph's on-disk transactional storage mode differs from in-memory approaches. We'll get into the implementation and distinctive benefits it brings to the table.

Memgraph utilizes [RocksDB](https://rocksdb.org/) as background storage to serialize nodes and relationships into a key-value format to achieve the on-disk transactional storage mode. This storage mode supports only the snapshot isolation level because it simplifies the query's execution flow since no data is transferred to the disk until the transaction is committed.

The durability is achieved with the help of RocksDB, which keeps its own WAL files. The imported data is on disk, while the main memory contains two caches—one for executing operations on the main RocksDB instance and the other for operations that require indexes. In both cases, Memgraph's custom SkipList cache is used, which allows a multithreaded read-write access pattern.

Concurrent transactions are handled differently in the on-disk storage mode than in the in-memory transactional storage mode. In the on-disk storage mode, the cache is used per transaction, so there is no need to question a certain object's validity, meaning the [optimistic approach](https://memgraph.com/docs/fundamentals/transactions#optimistic-vs-pessimistic-approaches) for conflict resolution between transactions is used.

In the on-disk storage mode, Deltas are still used to support Cypher's semantic of the write queries, but they are cleared after each transaction. That happens because the conflict is checked at the transaction’s commit time with RocksDB’s transaction support, which can optimize memory usage during execution. The design of the on-disk storage also simplifies the garbage collection process since all the data is on disk.

Before using on-disk storage mode, it is important to know the [implications](https://memgraph.com/docs/fundamentals/storage-memory-usage#implications-1). Although keeping the hardware costs to a minimum sounds perfect, this storage mode is still experimental because it does not offer the same performance as the in-memory transactional storage mode. If you try out on-disk transactional mode, keep in mind that while executing queries, all the graph objects used in the transactions still need to be able to fit in the RAM, or Memgraph will throw an exception.

## Choosing the Right Storage Mode for Your Needs

Which storage mode to use?

Deciding between Memgraph’s storage modes depends on your specific needs and the size of your data:

- **In-memory transactional storage mode** - Stick with this default mode if its performance meets your current needs. It’s fast and reliable, providing ACID guarantees for your transactions.

- **In-memory analytical storage mode** - Use this mode if ACID guarantees are not a priority and you’re looking to maximize performance and efficiency in memory usage. It’s ideal for analytical workloads where speed is of the essence.

- **On-disk transactional storage mode** - If your dataset exceeds your available memory, this mode offers a practical solution. It allows you to work with a subset of your data stored on disk, balancing between performance and capacity. However, be mindful of its experimental nature and the potential tradeoffs in performance compared to in-memory modes.

## Conclusion

Before making a switch, it’s important to understand the consequences of each storage mode on your workflows. Each has its benefits and limitations, affecting performance, data integrity, and how you manage your dataset.

**Need help?** If you are unsure which mode is best for you or if you have any questions, our DX team is here to help. Feel free to [schedule an office hour call](https://memgraph.com/office-hours) for personalized guidance. Additionally, our problem-solving [Discord community](https://www.discord.gg/memgraph) is a great resource for advice, tips, and discussions with fellow users and our team.

## Further Reading

- [Switch Storage Memory Modes](https://memgraph.com/docs/fundamentals/storage-memory-usage#switch-storage-modes)

- [Optimistic vs. Pessimistic Approaches](https://memgraph.com/docs/fundamentals/transactions#optimistic-vs-pessimistic-approaches)

- [Improve Query Execution Performance](https://memgraph.com/blog/improve-query-execution-performance)

- [In-memory vs. disk-based databases: Why do you need a larger than memory architecture?](https://memgraph.com/blog/in-memory-vs-disk-based-databases-larger-than-memory-architecture)

- [How to Import 1 Million Nodes and Edges per Second into Memgraph](https://memgraph.com/blog/how-to-import-1-milllion-nodes-and-edges-per-second-to-memgraph)





### Persistencia de datos en Memgraph con Docker (contenedor)

Para conservar los datos en Memgraph cuando se ejecuta en un contenedor Docker, debes usar **volúmenes de Docker**. Sin volúmenes, los datos se pierden al eliminar o recrear el contenedor.

#### Mecanismos de durabilidad

Memgraph usa dos mecanismos para garantizar la persistencia de los datos:

- **Write-ahead logging (WAL)**: cada modificación se registra en un archivo de log antes de escribirse en la base de datos.

- **Snapshots periódicos**: Memgraph crea instantáneas del estado completo de la base de datos en disco.

Estos archivos se guardan en `/var/lib/memgraph`. [[Data durability](https://memgraph.com/docs/fundamentals/data-durability)]

#### Cómo ejecutar Memgraph con persistencia de datos

Usa el flag `-v` para montar un volumen nombrado en la carpeta de datos:

`docker run -p 7687:7687 -p 7444:7444 -v mg_lib:/var/lib/memgraph memgraph/memgraph-mage`

Si también quieres persistir la configuración y los logs:

`docker run -p 7687:7687 -p 7444:7444 \ -v mg_lib:/var/lib/memgraph \ -v mg_etc:/etc/memgraph \ -v mg_log:/var/log/memgraph \ memgraph/memgraph-mage`

[[Persist data with Docker volumes](https://memgraph.com/docs/deployment/environments/docker#persist-data-with-docker-volumes)]

#### Ubicaciones importantes de datos

| Tipo de dato              | Ruta en el contenedor |
| ------------------------- | --------------------- |
| Datos del grafo           | `/var/lib/memgraph`   |
| Archivos de configuración | `/etc/memgraph`       |
| Logs                      | `/var/log/memgraph`   |
| Módulos de usuario        | `/usr/lib/memgraph`   |

#### Nota importante

Si no configuras un volumen, los datos **sí persisten mientras el contenedor exista** (reinicios), pero **se pierden si el contenedor es eliminado y recreado**. Los volúmenes nombrados son la práctica recomendada para entornos de producción. [[Persist data with Docker volumes](https://memgraph.com/docs/deployment/environments/docker#persist-data-with-docker-volumes)]

Answer based on the following sources:





# Data durability

Memgraph uses two mechanisms to ensure the durability of stored data and make disaster recovery possible:

- write-ahead logging (WAL)
- periodic snapshot creation

These mechanisms generate **durability files** and save them in the respective `wal` and `snapshots` folders in the **data directory**. Data directory stores permanent data on disk.

Memgraph **cannot be used with only WAL files enabled**. You can either have only snapshots or snapshots and WAL files.

The default data directory path is `/var/lib/memgraph` but the path can be changed by modifying the `--data-directory` configuration flag. To learn how to modify configuration flags, head over to the [Configuration](https://memgraph.com/docs/database-management/configuration#changing-configuration-settings) page.

With Memgraph Enterprise, the `data_directory` holds `databases` directory which splits durability files by database name. The reason for that is the multi-tenant architecture in Memgraph Enterprise, where the durability files for each database are stored under `/data_directory/databases/<db_name>`. The `databases` directory will exist even if you’re not using the multi-tenancy feature.

Durability files are deleted when certain events are triggered, for example, exceeding the maximum number of snapshots, defined by the `--storage-snapshot-retention-count=3` flag.

To prevent the deletion of durability files, you need to lock the `data directory`, and enable it again by unlocking the directory.

To manage this behavior, use the following queries:

```
LOCK DATA DIRECTORY;UNLOCK DATA DIRECTORY;
```

To show the status of the data directory, run:

```
DATA DIRECTORY LOCK STATUS;
```

To encrypt the data directory, use [LUKS](https://gitlab.com/cryptsetup/cryptsetup/) as it works with Memgraph out of the box and is undetectable from the application perspective so it shouldn’t break any existing applications.

## Durability mechanisms[](https://memgraph.com/docs/fundamentals/data-durability#durability-mechanisms)

To configure the durability mechanisms, check their respective [configuration flags](https://memgraph.com/docs/database-management/configuration#storage).

### Write-ahead logging[](https://memgraph.com/docs/fundamentals/data-durability#write-ahead-logging)

Write-ahead logging (WAL) is a technique applied in providing **atomicity** and **durability** to database systems.

In the default IN_MEMORY_TRANSACTIONAL [storage mode](https://memgraph.com/docs/fundamentals/storage-memory-usage#storage-modes), Memgraph creates a `Delta` object each time data is changed. By using Deltas, Memgraph creates write-ahead logs. Each database modification is therefore recorded in a log file before being written to the DB, and in the end the log file contains all steps needed to reconstruct the DB’s most recent state.

Memgraph has WAL enabled by default. To switch it on and off, use the boolean `--storage-wal-enabled` flag. For other WAL-related flags check the [configuration reference guide](https://memgraph.com/docs/database-management/configuration#storage).

By default, WAL files are located at `/var/lib/memgraph/wal`.

#### WAL file lifecycle

**Older WAL files are deleted automatically after a snapshot is created** since the snapshot contains the full database state up to that point. Only WAL files containing changes after the latest snapshot are retained.

To control WAL file cleanup indirectly, you can limit the number of snapshots via `--storage-snapshot-retention-count`.

**It is not possible to use WAL files exclusively** without snapshots. Memgraph enforces periodic snapshots when WAL is enabled and will fail to start if WAL is enabled with snapshot interval set to zero.

### Snapshots[](https://memgraph.com/docs/fundamentals/data-durability#snapshots)

Snapshots provide a faster way to restore the states of your database. Snapshots are created periodically based on the value defined with the `--storage-snapshot-interval` configuration flags, as well as upon exit based on the value of the `--storage-snapshot-on-exit` configuration flag. When a snapshot creation is triggered, the entire data storage is written to the drive. Nodes and relationships are divided into groups called batches.

If both flags `--storage-snapshot-interval` and `--storage-snapshot-interval-sec` are defined, the flag `--storage-snapshot-interval` will be used.

Snapshot creation can be made faster by using **multiple threads**. See [Parallelized execution](https://memgraph.com/docs/fundamentals/data-durability#parallelized-execution) for more information.

On startup, the database state is recovered from the most recent snapshot file. Memgraph can read the data and build the indexes on multiple threads, using batches as a parallelization unit: each thread will recover one batch at a time until there are no unhandled batches.

This means the same batch size might not be suitable for every dataset. A smaller dataset might require a smaller batch size to utilize a multi-threaded processor, while bigger datasets might use bigger batches to minimize the synchronization between the worker threads. Therefore, the size of batches and the number of used threads [are configurable](https://memgraph.com/docs/database-management/configuration#storage) similarly to other durability-related settings.

The timestamp of the snapshot is compared with the latest update recorded in the WAL file and, if the snapshot is less recent, the state of the DB will be recovered using the WAL file.

Memgraph has snapshot creation enabled by default. You can configure the exact snapshot creation behavior by [defining the relevant flags](https://memgraph.com/docs/database-management/configuration#storage). Alternatively, you can make one directly by running the following query:

```
CREATE SNAPSHOT;
```

If another snapshot is already being created or no committed writes to the database have been made since the last snapshot, this query will fail with an error.

By default, snapshot files are saved inside the `var/lib/memgraph/snapshots` directory. The `CREATE SNAPSHOT` query will return the path of the newly created snapshot file.

To query which snapshots currently exist in the data directory, execute:

```
SHOW SNAPSHOTS;
```

#### Snapshot and WAL recovery logic

During recovery, Memgraph always attempts to use the fastest and most efficient method to restore the database state:

- If the snapshot has a **more recent** timeline than the WAL, the database is fully recovered from the latest snapshot.
- If the snapshot has a **less recent** timeline than the WAL, Memgraph first recovers from the snapshot, and then replays WAL files containing changes made after the snapshot was taken. This ensures recovery to the most recent state.
- Snapshot recovery is **typically faster** than recovery from WAL because snapshots store the complete state of the database in a single file, while WAL files store incremental changes and need to be replayed sequentially.

### Periodic snapshots[](https://memgraph.com/docs/fundamentals/data-durability#periodic-snapshots)

`IN_MEMORY_TRANSACTIONAL` mode supports periodic snapshot creation. The interval can be set at startup via the `--storage-snapshot-interval` flag or at run-time via the database settings:

```
SET DATABASE SETTING "storage.snapshot.interval" TO "1200";SET DATABASE SETTING "storage.snapshot.interval" TO "* * 12 * * *";SET DATABASE SETTING "storage.snapshot.interval" TO "";
```

Changing the configuration settings depends on the way you are using Memgraph, so please refer to the [configuration docs](https://memgraph.com/docs/database-management/configuration#changing-configuration) for more information.

If the interval string is an integer, then it’s treated as the execution period in seconds. Interval can also be defined as a 6-field CRON expression (seconds, minute, hour, day of month, month, day of week). Standard 5-field cron references (e.g. [crontab.guru](https://crontab.guru/)) describe the last five fields; Memgraph adds seconds as the first field. By setting the value to an empty string, the background process is paused and any currently active snapshot creation will finish. Please note that defining the interval via a CRON expression is an [Enterprise feature](https://memgraph.com/docs/database-management/enabling-memgraph-enterprise).

If the database is started in or migrated into `IN_MEMORY_ANALYTICAL` mode, the background thread will pause and no snapshots will be created as long as that mode is active. The job will continue with the last defined interval when the storage mode is changed to `IN_MEMORY_TRANSACTIONAL` storage mode.

The periodic snapshot will be skipped if another snapshot is in progress or no new writes have been committed since the last snapshot. If the periodic snapshot is skipped it will be logged on INFO level.

Snapshots and WAL files are presently not compatible between Memgraph versions.

### Parallelized execution[](https://memgraph.com/docs/fundamentals/data-durability#parallelized-execution)

Snapshot creation in Memgraph can be optimized using multiple threads, which significantly reduces the time required to create snapshots for large datasets.

This behavior can be controlled using the following flags:

- `--storage-parallel-snapshot-creation`: This flag determines whether snapshot creation is performed in a multi-threaded fashion. By default, it is set to `false`. To enable parallelized execution, set this flag to `true`.
- `--storage-snapshot-thread-count`: This flag specifies the number of threads to be used for snapshot creation. By default, Memgraph uses the system’s maximum thread count. You can override this value to fine-tune performance based on your system’s resources.

When parallelized execution is enabled, Memgraph divides the data into batches, where the batch size is defined via `--storage-items-per-batch`. The optimal batch size and thread count may vary depending on the dataset size and system configuration.

#### When parallelization helps

Parallel execution is especially beneficial when CPU-bound operations dominate the snapshot creation process, such as serialization or compression of in-memory structures. As a general guideline, parallel snapshot creation provides the most significant performance improvement when disk I/O constitutes 25% or less of the total snapshot creation time.

To take full advantage of parallelization, it’s also important to set the `--storage-items-per-batch` flag appropriately. This value determines how the dataset is split into work units for threads. A good rule of thumb is: Total number of items (vertices + edges) ≈ 4 × number of threads × —storage-items-per-batch This ensures that each thread has enough batches to work on without idling, helping maximize CPU utilization during snapshot creation.

When using multi-threaded snapshot creation with the correct batch size, the disk will once again become the bottleneck. At that point, more threads will not necessarily yield better performance.

#### Measuring disk write speed on Linux

To determine how fast your disk can handle writes (which influences the I/O bottleneck), you can use the dd command:

```
dd if=/dev/zero of=testfile bs=1G count=1 oflag=direct
```

This writes a 1 GB file directly to disk and reports the write speed. After the test, remove the file.

You can also monitor real-time disk utilization during snapshot creation using tools like `iostat`, `iotop`, or `dstat`.

## Storage modes[](https://memgraph.com/docs/fundamentals/data-durability#storage-modes)

Memgraph has the option to work in `IN_MEMORY_ANALYTICAL`, `IN_MEMORY_TRANSACTIONAL` or `ON_DISK_TRANSACTIONAL` [storage modes](https://memgraph.com/docs/fundamentals/storage-memory-usage).

Memgraph always starts in the `IN_MEMORY_TRANSACTIONAL` mode in which it creates periodic snapshots and write-ahead logging as durability mechanisms, and also enables creating manual snapshots.

In the `IN_MEMORY_ANALYTICAL` mode, Memgraph offers no periodic snapshots and write-ahead logging. Users can create a snapshot with the `CREATE SNAPSHOT;` Cypher query. During the process of snapshot creation, other transactions will be prevented from starting until the snapshot creation is completed.

In the `ON_DISK_TRANSACTIONAL` mode, durability is supported by RocksDB since it keeps its own [WAL](https://github.com/facebook/rocksdb/wiki/Write-Ahead-Log-%28WAL%29) files. Memgraph persists the metadata used in the implementation of the on-disk storage.





## Persist data with Docker volumes[](https://memgraph.com/docs/deployment/environments/docker#persist-data-with-docker-volumes)

Docker volumes are used for data persistence across container lifecycles, data sharing between containers, efficient data storage, backup and migration and for easy access from the host system.

Whenever you restart your Docker container, the container’s filesystem will persist your data, logs and configuration. Still, data will not be persisted across container deletion and recreation. To ensure you have your data even if you decide to spin up a new container, run the container with volumes.

Volumes are the preferred mechanism for persisting data generated by and used by Docker containers. They are completely managed by Docker and are stored outside of the default filesystem. The data in volumes is preserved across container restarts and can be shared between multiple containers.

Although bind mounts, which allow you to attach specific paths from your host machine to paths in the container, are also used for data persistence, they are not a recommended option.

The best practice to ensure volume data persistence is to use named volumes and to do regular backups.

Here are the locations of the different types of data that Memgraph uses:

- Configuration files: `/etc/memgraph`
- Logs: `/var/log/memgraph`
- User-related data: `/usr/lib/memgraph`
- Graph data: `/var/lib/memgraph`

Here is the command to run Memgraph with volumes for data persistency:

```
docker run -p 7687:7687 -p 7444:7444 -v mg_lib:/var/lib/memgraph memgraph/memgraph-mage
```

Commonly, you want to ensure you have the same Memgraph configuration wherever you start it. Then you can add volume for the configuration persistency as well:

```
docker run -p 7687:7687 -p 7444:7444 -v mg_lib:/var/lib/memgraph -v mg_etc:/etc/memgraph memgraph/memgraph-mage
```

If you’d like an easy access to logs on your machine, you can add volume for logs as well:

```
docker run -p 7687:7687 -p 7444:7444 -v mg_lib:/var/lib/memgraph -v mg_etc:/etc/memgraph -v mg_log:/var/log/memgraph memgraph/memgraph-mage
```

Named volumes are Docker-managed volumes that store data independently of containers. They are not directly mapped to a specific host directory that you choose because, in this case, Docker manages where the data is stored on the host. However, you can still access this data from the host.

As opposed to bind mounts, named volumes provide better encapsulation and separation of the environment. Having named volumes makes it easier to back up or migrate data. Since they’re managed by Docker, there is an additional layer of abstraction and security. Named volumes are more suitable for production deployments, where security, data integrity, and portability are critical.

If you want to start a new Memgraph instance with the data from another Docker container which has `mg_lib` volume attached to it, you can run the following command:

```
docker run -p 7687:7687 -p 7444:7444 -v mg_lib:/var/lib/memgraph memgraph/memgraph-mage
```

The new container will be started with the contents from the `mg_lib` volume, meaning it will restore the database from the existing snapshots. That’s the easiest way to transfer your data to another instance.

Additionally, here are some useful facts about Docker volumes:

- Two containers can’t use the same volume at the same time: Be careful when you run a new Memgraph instance to change the name of the volume if you plan on running two Memgraph instances at the same time with different data.
- Two containers can use the same volume if they’re not running at the same time: you can run a new Memgraph instance with an already used volume if you first stopped a previously running instance. That is useful when you want to reuse the same data for two instances.
- Using named volumes is the easiest way to migrate data between different containers.
- With named volumes, you can save files locally by inspecting the volume and saving the data to the local machine. With Docker Desktop, these actions are straightforward. Docker volumes can be inspected even when the container is down.

[Learn more about Docker](https://memgraph.com/docs/getting-started/first-steps-with-docker)

## Backup data[](https://memgraph.com/docs/deployment/environments/docker#backup-data)

All your data is stored in the `/var/lib/memgraph` data folder. Although being in-memory, Memgraph creates snapshots and WAL files to persist your data. Because of that, it is a good practice to have a named volume on the `/var/lib/memgraph` folder. That volume can be attached to a new instance, which will then start with your data being loaded.

Still, it is a good practice to do a backup regularly.

### Copy the data persistence folder[](https://memgraph.com/docs/deployment/environments/docker#copy-the-data-persistence-folder)

To create a backup, you need to copy the contents of `/var/lib/memgraph` folder. If you previously set up the volume on `/var/lib/memgraph` data folder, then just save the content from that volume on a safe location.

If you didn’t run Memgraph with set up volumes, then copy the contents of `/var/lib/memgraph` folder to a safe location. To do that, use `docker cp` command. For example, to copy the whole data folder from Memgraph onto the local file system, first run the following query in Memgraph to lock the data directory to avoid changes happening during the backup process:

```
LOCK DATA DIRECTORY;
```

After that, copy the data folder onto your local file system:

```
docker cp <container_id>:/var/lib/memgraph /path/to/my/local-folder
```

In the end, unlock the data directory by running the following query in Memgraph:

```
UNLOCK DATA DIRECTORY;
```

By default, Memgraph creates snapshots every 300 seconds and retains three latest snapshots, so it can easily recover in case of corruption. It is a good practice to have more than one snapshot. If something caused the database to crash, Memgraph will still be able to recover your data from the write-ahead logs. On exit, Memgraph will create the latest snapshot. This can be [configured](https://memgraph.com/docs/database-management/configuration#storage), based on your dataset size and use case. If your data is not being frequently updated, you can disable periodic snapshot creation and create snapshots manually when you need to.

### Dump database[](https://memgraph.com/docs/deployment/environments/docker#dump-database)

Another approach is to dump the database into a file. That is useful if you want to move the data between different Memgraph versions that might have incompatible data formats are used for snapshots or WAL files.

Here are the steps to dump the database with Memgraph running in a Docker container:

1. `docker exec -it -u 0 <container_id> bash`
2. `echo "DUMP DATABASE;" | mgconsole --output-format=cypherl > data.cypherl`
3. `docker cp <container_id>:data.cypherl data.cypherl`

The whole graph is dumped into a CYPHERL file, which consists of Cypher queries used to create a database.

It is a better practice to copy the data persistency folder when possible over dumping the database since both the backup and restore processes are significantly faster.

## Restore data[](https://memgraph.com/docs/deployment/environments/docker#restore-data)

Depending on the backup method you use, you can restore data differently. If you set up a volume on `var/lib/memgraph` directory, then you can attach it to the new container. If you didn’t set up a volume on `var/lib/memgraph` directory, then you need to copy the data folder’s contents in the new container in `var/lib/memgraph` directory.

The Memgraph user should own the backup data folder, so make sure the folder is accessible for read and write operations by the Memgraph user.

If you have dumped the database, you can import the data back into Memgraph using the mgconsole CLI tool or the client library. Make sure you read the [best practices for such import](https://memgraph.com/docs/data-migration/best-practices#cypher-queries-best-practices).

### Upgrading Memgraph[](https://memgraph.com/docs/deployment/environments/docker#upgrading-memgraph)

Between different versions of Memgraph, we might break the compatibility of the configurations, snapshots, and WAL files. That is done very rarely, but it is helpful to keep an eye on the [release notes](https://memgraph.com/docs/release-notes) to see if there are any breaking changes.

## Set up a cluster[](https://memgraph.com/docs/deployment/environments/docker#set-up-a-cluster)

To create a cluster, replicate data across several instances. Setting up replication means running a couple of Memgraph instances, where one of them is the MAIN instance, and others are either SYNC or ASYNC replicas.

Here is an example of setting up a replication cluster with three instances:

Run the instance on port 7687 (this instance will be MAIN):

```
docker run -p 7687:7687 -p 7444:7444 -p 10000:10000 memgraph/memgraph-mage --replication-restore-state-on-startup=true
```

Run another instance on port 7688 (this instance will be REPLICA):

```
docker run -p 7688:7687 -p 7445:7444 -p 10000:10000 memgraph/memgraph-mage --replication-restore-state-on-startup=true
```

Run the last instance on port 7689 (this instance will be REPLICA):

```
docker run -p 7689:7687 -p 7446:7444 -p 10000:10000 memgraph/memgraph-mage --replication-restore-state-on-startup=true
```

All started instances are MAIN upon starting. To set up a cluster, two instances must be demoted to REPLICA roles because only one instance can be MAIN. To do that, run the following query from the second and third instance (REPLICA instances):

```
SET REPLICATION ROLE TO REPLICA WITH PORT 10000;
```

To finish setting up the replication cluster, you need to register REPLICA instances from the MAIN instance with the correct IP addresses or DNS of REPLICA instances:

```
REGISTER REPLICA REP1 SYNC TO "<IP_ADDRESS_REP1>";REGISTER REPLICA REP2 ASYNC TO "<IP_ADDRESS_REP2>";
```

If you have trouble connecting, check your firewall settings.

That’s it, replication cluster with one MAIN, one SYNC REPLICA and one ASYNC REPLICA instance is set up. To learn more about the replication Memgraph, refer to our [replication docs](https://memgraph.com/docs/clustering/replication#set-up-a-replication-cluster).

Having the replication cluster set up is great if you need to replicate data, add load balancing or improve availability. Still, to achieve high availability, you need to manage automatic failover. On the other hand, Memgraph Enterprise has a high availability feature included in the offering to ease the management of Memgraph cluster. In such case, the cluster consists of MAIN instance, REPLICA instances and COORDINATOR instances, which, backed up by Raft protocol, manage the cluster state.

[Learn more about high availability](https://memgraph.com/docs/clustering/high-availability)

## Logging[](https://memgraph.com/docs/deployment/environments/docker#logging)

At any point in your Memgraph instance lifecycle, you might need to check the logs either to debug an issue or to monitor the performance. Memgraph logs are stored in the `/var/log/memgraph` folder if the default location is not changed by the `--log-file` flag. They are typically stored in the format `memgraph_year-month-day.log`.

You can control the log level as described on the [logs page](https://memgraph.com/docs/database-management/logs). If you are setting up the production environment, you should consider setting the log level to `INFO` or `WARNING` to avoid the log files growing too large.

If you are experiencing some issues or you have trouble setting up the Memgraph instance, consider setting the log level to `TRACE` to get more information about the issue.

If you created a volume on `/var/log/memgraph` folder, you can inspect it to access logs.

The best way to monitor logs is to attach the logs directly to your terminal as you debug the issue. You can do that by running the following command:

```
docker logs -f <CONTAINER>
```

Because of flag `-f` or `--follow`, the above command will continue streaming the new output from the container’s `STDOUT` and `STDERR`.

More on the `docker logs` command can be found on the [Docker documentation](https://docs.docker.com/reference/cli/docker/container/logs/).

## Where to next?[](https://memgraph.com/docs/deployment/environments/docker#where-to-next)

Docker is a powerful tool, and it is usually a good starting point. If your application involves multiple services besides a database, you might want to create a multi-container application with Docker Compose. To learn more about how to manage Memgraph in such an environment, follow our Docker Compose guide.

To discuss Docker and similar topics, [join our Discord community](https://www.discord.gg/memgraph).

Schedule a 30-min session with our engineers to discuss how Memgraph fits with your architecture. Our engineers are highly experienced in helping companies of all sizes to integrate and get the most out of Memgraph in their projects. Talk to us about data modeling, optimizing queries, defining infrastructure requirements or migrating from your existing graph database. No nonsense or sales pitch, just tech.





# Data durability

Memgraph uses two mechanisms to ensure the durability of stored data and make disaster recovery possible:

- write-ahead logging (WAL)
- periodic snapshot creation

These mechanisms generate **durability files** and save them in the respective `wal` and `snapshots` folders in the **data directory**. Data directory stores permanent data on disk.

Memgraph **cannot be used with only WAL files enabled**. You can either have only snapshots or snapshots and WAL files.

The default data directory path is `/var/lib/memgraph` but the path can be changed by modifying the `--data-directory` configuration flag. To learn how to modify configuration flags, head over to the [Configuration](https://memgraph.com/docs/database-management/configuration#changing-configuration-settings) page.

With Memgraph Enterprise, the `data_directory` holds `databases` directory which splits durability files by database name. The reason for that is the multi-tenant architecture in Memgraph Enterprise, where the durability files for each database are stored under `/data_directory/databases/<db_name>`. The `databases` directory will exist even if you’re not using the multi-tenancy feature.

Durability files are deleted when certain events are triggered, for example, exceeding the maximum number of snapshots, defined by the `--storage-snapshot-retention-count=3` flag.

To prevent the deletion of durability files, you need to lock the `data directory`, and enable it again by unlocking the directory.

To manage this behavior, use the following queries:

```
LOCK DATA DIRECTORY;UNLOCK DATA DIRECTORY;
```

To show the status of the data directory, run:

```
DATA DIRECTORY LOCK STATUS;
```

To encrypt the data directory, use [LUKS](https://gitlab.com/cryptsetup/cryptsetup/) as it works with Memgraph out of the box and is undetectable from the application perspective so it shouldn’t break any existing applications.

## Durability mechanisms[](https://memgraph.com/docs/fundamentals/data-durability#durability-mechanisms)

To configure the durability mechanisms, check their respective [configuration flags](https://memgraph.com/docs/database-management/configuration#storage).

### Write-ahead logging[](https://memgraph.com/docs/fundamentals/data-durability#write-ahead-logging)

Write-ahead logging (WAL) is a technique applied in providing **atomicity** and **durability** to database systems.

In the default IN_MEMORY_TRANSACTIONAL [storage mode](https://memgraph.com/docs/fundamentals/storage-memory-usage#storage-modes), Memgraph creates a `Delta` object each time data is changed. By using Deltas, Memgraph creates write-ahead logs. Each database modification is therefore recorded in a log file before being written to the DB, and in the end the log file contains all steps needed to reconstruct the DB’s most recent state.

Memgraph has WAL enabled by default. To switch it on and off, use the boolean `--storage-wal-enabled` flag. For other WAL-related flags check the [configuration reference guide](https://memgraph.com/docs/database-management/configuration#storage).

By default, WAL files are located at `/var/lib/memgraph/wal`.

#### WAL file lifecycle

**Older WAL files are deleted automatically after a snapshot is created** since the snapshot contains the full database state up to that point. Only WAL files containing changes after the latest snapshot are retained.

To control WAL file cleanup indirectly, you can limit the number of snapshots via `--storage-snapshot-retention-count`.

**It is not possible to use WAL files exclusively** without snapshots. Memgraph enforces periodic snapshots when WAL is enabled and will fail to start if WAL is enabled with snapshot interval set to zero.

### Snapshots[](https://memgraph.com/docs/fundamentals/data-durability#snapshots)

Snapshots provide a faster way to restore the states of your database. Snapshots are created periodically based on the value defined with the `--storage-snapshot-interval` configuration flags, as well as upon exit based on the value of the `--storage-snapshot-on-exit` configuration flag. When a snapshot creation is triggered, the entire data storage is written to the drive. Nodes and relationships are divided into groups called batches.

If both flags `--storage-snapshot-interval` and `--storage-snapshot-interval-sec` are defined, the flag `--storage-snapshot-interval` will be used.

Snapshot creation can be made faster by using **multiple threads**. See [Parallelized execution](https://memgraph.com/docs/fundamentals/data-durability#parallelized-execution) for more information.

On startup, the database state is recovered from the most recent snapshot file. Memgraph can read the data and build the indexes on multiple threads, using batches as a parallelization unit: each thread will recover one batch at a time until there are no unhandled batches.

This means the same batch size might not be suitable for every dataset. A smaller dataset might require a smaller batch size to utilize a multi-threaded processor, while bigger datasets might use bigger batches to minimize the synchronization between the worker threads. Therefore, the size of batches and the number of used threads [are configurable](https://memgraph.com/docs/database-management/configuration#storage) similarly to other durability-related settings.

The timestamp of the snapshot is compared with the latest update recorded in the WAL file and, if the snapshot is less recent, the state of the DB will be recovered using the WAL file.

Memgraph has snapshot creation enabled by default. You can configure the exact snapshot creation behavior by [defining the relevant flags](https://memgraph.com/docs/database-management/configuration#storage). Alternatively, you can make one directly by running the following query:

```
CREATE SNAPSHOT;
```

If another snapshot is already being created or no committed writes to the database have been made since the last snapshot, this query will fail with an error.

By default, snapshot files are saved inside the `var/lib/memgraph/snapshots` directory. The `CREATE SNAPSHOT` query will return the path of the newly created snapshot file.

To query which snapshots currently exist in the data directory, execute:

```
SHOW SNAPSHOTS;
```

#### Snapshot and WAL recovery logic

During recovery, Memgraph always attempts to use the fastest and most efficient method to restore the database state:

- If the snapshot has a **more recent** timeline than the WAL, the database is fully recovered from the latest snapshot.
- If the snapshot has a **less recent** timeline than the WAL, Memgraph first recovers from the snapshot, and then replays WAL files containing changes made after the snapshot was taken. This ensures recovery to the most recent state.
- Snapshot recovery is **typically faster** than recovery from WAL because snapshots store the complete state of the database in a single file, while WAL files store incremental changes and need to be replayed sequentially.

### Periodic snapshots[](https://memgraph.com/docs/fundamentals/data-durability#periodic-snapshots)

`IN_MEMORY_TRANSACTIONAL` mode supports periodic snapshot creation. The interval can be set at startup via the `--storage-snapshot-interval` flag or at run-time via the database settings:

```
SET DATABASE SETTING "storage.snapshot.interval" TO "1200";SET DATABASE SETTING "storage.snapshot.interval" TO "* * 12 * * *";SET DATABASE SETTING "storage.snapshot.interval" TO "";
```

Changing the configuration settings depends on the way you are using Memgraph, so please refer to the [configuration docs](https://memgraph.com/docs/database-management/configuration#changing-configuration) for more information.

If the interval string is an integer, then it’s treated as the execution period in seconds. Interval can also be defined as a 6-field CRON expression (seconds, minute, hour, day of month, month, day of week). Standard 5-field cron references (e.g. [crontab.guru](https://crontab.guru/)) describe the last five fields; Memgraph adds seconds as the first field. By setting the value to an empty string, the background process is paused and any currently active snapshot creation will finish. Please note that defining the interval via a CRON expression is an [Enterprise feature](https://memgraph.com/docs/database-management/enabling-memgraph-enterprise).

If the database is started in or migrated into `IN_MEMORY_ANALYTICAL` mode, the background thread will pause and no snapshots will be created as long as that mode is active. The job will continue with the last defined interval when the storage mode is changed to `IN_MEMORY_TRANSACTIONAL` storage mode.

The periodic snapshot will be skipped if another snapshot is in progress or no new writes have been committed since the last snapshot. If the periodic snapshot is skipped it will be logged on INFO level.

Snapshots and WAL files are presently not compatible between Memgraph versions.

### Parallelized execution[](https://memgraph.com/docs/fundamentals/data-durability#parallelized-execution)

Snapshot creation in Memgraph can be optimized using multiple threads, which significantly reduces the time required to create snapshots for large datasets.

This behavior can be controlled using the following flags:

- `--storage-parallel-snapshot-creation`: This flag determines whether snapshot creation is performed in a multi-threaded fashion. By default, it is set to `false`. To enable parallelized execution, set this flag to `true`.
- `--storage-snapshot-thread-count`: This flag specifies the number of threads to be used for snapshot creation. By default, Memgraph uses the system’s maximum thread count. You can override this value to fine-tune performance based on your system’s resources.

When parallelized execution is enabled, Memgraph divides the data into batches, where the batch size is defined via `--storage-items-per-batch`. The optimal batch size and thread count may vary depending on the dataset size and system configuration.

#### When parallelization helps

Parallel execution is especially beneficial when CPU-bound operations dominate the snapshot creation process, such as serialization or compression of in-memory structures. As a general guideline, parallel snapshot creation provides the most significant performance improvement when disk I/O constitutes 25% or less of the total snapshot creation time.

To take full advantage of parallelization, it’s also important to set the `--storage-items-per-batch` flag appropriately. This value determines how the dataset is split into work units for threads. A good rule of thumb is: Total number of items (vertices + edges) ≈ 4 × number of threads × —storage-items-per-batch This ensures that each thread has enough batches to work on without idling, helping maximize CPU utilization during snapshot creation.

When using multi-threaded snapshot creation with the correct batch size, the disk will once again become the bottleneck. At that point, more threads will not necessarily yield better performance.

#### Measuring disk write speed on Linux

To determine how fast your disk can handle writes (which influences the I/O bottleneck), you can use the dd command:

```
dd if=/dev/zero of=testfile bs=1G count=1 oflag=direct
```

This writes a 1 GB file directly to disk and reports the write speed. After the test, remove the file.

You can also monitor real-time disk utilization during snapshot creation using tools like `iostat`, `iotop`, or `dstat`.

## Storage modes[](https://memgraph.com/docs/fundamentals/data-durability#storage-modes)

Memgraph has the option to work in `IN_MEMORY_ANALYTICAL`, `IN_MEMORY_TRANSACTIONAL` or `ON_DISK_TRANSACTIONAL` [storage modes](https://memgraph.com/docs/fundamentals/storage-memory-usage).

Memgraph always starts in the `IN_MEMORY_TRANSACTIONAL` mode in which it creates periodic snapshots and write-ahead logging as durability mechanisms, and also enables creating manual snapshots.

In the `IN_MEMORY_ANALYTICAL` mode, Memgraph offers no periodic snapshots and write-ahead logging. Users can create a snapshot with the `CREATE SNAPSHOT;` Cypher query. During the process of snapshot creation, other transactions will be prevented from starting until the snapshot creation is completed.

In the `ON_DISK_TRANSACTIONAL` mode, durability is supported by RocksDB since it keeps its own [WAL](https://github.com/facebook/rocksdb/wiki/Write-Ahead-Log-%28WAL%29) files. Memgraph persists the metadata used in the implementation of the on-disk storage.

[Data types](https://memgraph.com/docs/fundamentals/data-types "Data types")



# Backup and restore

Memgraph uses snapshots and WAL to ensure the [durability](https://memgraph.com/docs/fundamentals/data-durability) of the stored data. Learn how to safely backup and restore your data.

## Create backup[](https://memgraph.com/docs/database-management/backup-and-restore#create-backup)

Follow these steps to create database backup:

### Create a snapshot

If necessary, create a snapshot of the current database state by running the following query in `mgconsole` or Memgraph Lab:

```
CREATE SNAPSHOT;
```

The snapshot is saved in the `snapshots` directory of the data directory (`/var/lib/memgraph`).

### Lock the data directory

Durability files are deleted when an event is triggered, for example, exceeding the maximum number of snapshots.

To disable this behavior, run the following query in `mgconsole` or Memgraph Lab:

```
LOCK DATA DIRECTORY;
```

### Copy files

Copy snapshot files (from the `snapshots` directory) and any additional WAL files (from the `wal` directory) to a backup location.

If you’ve just created a snapshot file there is no need to backup WAL files.

To copy the snapshot files from the Docker container first check the container ID by running `docker ps` then run the following command:

```
 docker cp  <CONTAINER ID>:/var/lib/memgraph/snapshots/<snapshot_file> <snapshot_file>
```

### Unlock the data directory

Run the following query in `mgconsole` or Memgraph Lab to unlock the directory:

```
UNLOCK DATA DIRECTORY;
```

Memgraph will delete the files which should have been deleted before locking and allow any future deletion of the durability files.

## Restore data[](https://memgraph.com/docs/database-management/backup-and-restore#restore-data)

Restore a snapshot to a running Memgraph instance using the RECOVER SNAPSHOT command:

```
RECOVER SNAPSHOT path=literal ( WITH CONFIG configsMap=configMap ) ? ( FORCE )? ;
```

Before modifying the local data directory, Memgraph will move all existing WALs and snapshots to a hidden `.old` directory. This directory is reused for subsequent recovery operations, meaning **only a single backup is maintained at any time**. Files already present in the `.old` directory will be deleted before moving the current files, ensuring only the most recent backup is preserved. By default, snapshots are stored in the local directory `/var/lib/memgraph/snapshots/`.

Snapshots can be recovered from:

- Local filesystem - absolute or relative paths
- S3-compatible storage - s3://bucket/path/to/snapshot
- Remote servers - http://, https://, or ftp:// URLs

### Local filesystem[](https://memgraph.com/docs/database-management/backup-and-restore#local-filesystem)

```
RECOVER SNAPSHOT "/path/to/snapshot";
```

Use absolute paths when possible. Relative paths are resolved from the Memgraph execution directory. Memgraph copies the snapshot to its local snapshot directory, so ensure the file has appropriate read permissions.

If not, you might encounter the following error:

```
Failed to copy snapshot over to local snapshots directory.
```

### S3-compatible storage[](https://memgraph.com/docs/database-management/backup-and-restore#s3-compatible-storage)

Provide AWS credentials using one of these methods (in order of precedence):

| Method                | Example                                                                   |
| --------------------- | ------------------------------------------------------------------------- |
| Query config          | `WITH CONFIG {aws_region: ..., aws_access_key: ..., aws_secret_key: ...}` |
| Environment variables | `AWS_REGION`, `AWS_ACCESS_KEY`, `AWS_SECRET_KEY`, `AWS_ENDPOINT_URL`      |
| Runtime settings      | `aws.region`, `aws.access_key`, `aws.secret_key`, `aws.endpoint_url`      |

Example:

```
RECOVER SNAPSHOT "s3://my-bucket/snapshots/backup.snapshot" WITH CONFIG {'aws_region': 'eu-west-1', 'aws_access_key': '...', 'aws_secret_key': 'secret'};
```

### The FORCE flag[](https://memgraph.com/docs/database-management/backup-and-restore#the-force-flag)

If the instance is not freshly started, add the `FORCE` flag to your command:

```
RECOVER SNAPSHOT "/path/to/snapshot" FORCE;
```

This will clear all existing data before applying the snapshot.

In order to query the snapshots currently present in the local data directory, execute the query:

```
SHOW SNAPSHOTS;
```

Its results contain the path to the file, the logical timestamp, the physical timestamp and the file size.

As of Memgraph v3.5, the `SHOW SNAPSHOTS` query does not return information regarding the next scheduled snapshot. A special query has been added:

```
SHOW NEXT SNAPSHOT;
```

If the periodic snapshot background job is active, the result will return the path and the time at which the snapshots will be created.

If you are using Memgraph pre v2.22, follow these steps to restore data from a backup:

### Empty the `wal` directory

If you want to restore data only from the snapshot file, ensure that the `wal` directory is empty:

1. Find the container ID using a `docker ps` command, then enter the container using:

```
docker exec -it CONTAINER_ID bash
```

2. Position yourself in the `/var/lib/memgraph/wal` directory and `rm *`

### Stop the instance

Run the following command

```
docker stop CONTAINER_ID
```

### Start the instance

You can start the instance with the backed up files in two ways.

#### Option 1

You can start the instance by adding a `-v ~/snapshots:/var/lib/memgraph/snapshots` flag to the `docker run` command, where the `~/snapshots` represents a path to the location of the directory with the back-up snapshot, for example:

```
docker run -p 7687:7687 -p 7444:7444 -v ~/snapshots:/var/lib/memgraph/snapshots memgraph/memgraph
```

If you want to copy both WAL and snapshot files start the instance by adding a `-v ~/snapshots:/var/lib/memgraph/snapshots -v ~/wal:/var/lib/memgraph/wal` flags to the `docker run` command, where the `~/snapshots` represents a path to the location of the backed-up snapshot directory, and `~/wal` represents a path to the location of the backed-up wal directory for example:

```
docker run -p 7687:7687 -p 7444:7444 -v ~/snapshots:/var/lib/memgraph/snapshots -v ~/wal:/var/lib/memgraph/wal memgraph/memgraph
```

#### Option 2

The other option is to copy the backed-up snapshot file into the `snapshots` directory after creating the container and start the database. So the commands should look like this:

```
docker create -p 7687:7687 -p 7444:7444 -v `snapshots`:/var/lib/memgraph/snapshots --name memgraphDB memgraph/memgraphtar -cf - sample_snapshot_file | docker cp -a - memgraphDB:/var/lib/memgraph/snapshots
```

The `sample_snapshot_file` is the snapshot file you want to use to restore the data. Due to the nature of Docker file ownership, you need to use `tar` to copy the file as STDIN into the non-running container. It will allow you to change the ownership of the file to the `memgraph` user inside the container.

After that, start the database with:

```
docker start -a memgraphDB
```

The `-a` flag is used to attach to the container’s output so you can see the logs.

Once memgraph is started, change the snapshot directory ownership to the `memgraph` user by running the following command:

```
docker exec -it -u 0 memgraphDB bash -c "chown memgraph:memgraph /var/lib/memgraph/snapshots"
```

Otherwise, Memgraph will not be able to write the future snapshot files and will fail.

## Database dump[](https://memgraph.com/docs/database-management/backup-and-restore#database-dump)

The database dump contains a record of the database state in the form of Cypher queries. It’s equivalent to the SQL dump in relational DBs. Database dump preserves nodes, relationships, indexes, constraints and triggers.

You can run the queries constituting the dump to recreate the state of the DB as it was at the time of the dump.

To dump the Memgraph DB, run the following query:

```
DUMP DATABASE;
```

If you are using Memgraph Lab, you can dump the database, that is, the queries to recreate it, to a CYPHERL file in the `Import & Export` section of the Lab.

## Storage modes[](https://memgraph.com/docs/database-management/backup-and-restore#storage-modes)

Memgraph has the option to work in `IN_MEMORY_ANALYTICAL`, `IN_MEMORY_TRANSACTIONAL` or `ON_DISK_TRANSACTIONAL` [storage modes](https://memgraph.com/docs/fundamentals/storage-memory-usage).

Memgraph always starts in the `IN_MEMORY_TRANSACTIONAL` mode in which it creates periodic snapshots and write-ahead logging as durability mechanisms, and also enables creating manual snapshots.

In the `IN_MEMORY_ANALYTICAL` mode, Memgraph offers no periodic snapshots and write-ahead logging. Users can create a snapshot with the `CREATE SNAPSHOT;` Cypher query. During the process of snapshot creation, other transactions will be prevented from starting until the snapshot creation is completed.

In the `ON_DISK_TRANSACTIONAL` mode, durability is supported by RocksDB since it keeps its own [WAL](https://github.com/facebook/rocksdb/wiki/Write-Ahead-Log-%28WAL%29) files. Memgraph persists the metadata used in the implementation of the on-disk storage.

## Backup in multi-tenancy Enterprise[](https://memgraph.com/docs/database-management/backup-and-restore#backup-in-multi-tenancy-enterprise)

When running Memgraph with multi-tenancy, every database other than the default database (named `memgraph`) will have its own associated database UUID. Database UUID can be inspected by running the `SHOW STORAGE INFO` command and reading the value under the `database_uuid` key. The default data directory location for a specific database is `/var/lib/memgraph/<database_uuid>/`. The default database `memgraph` does not follow this directory structure and the data files are directly located under `/var/lib/memgraph`.

Manual snapshot backup flow should look like this:

### Create snapshots inside Memgraph

Create snapshot for every database (or let it create automatically with periodic snapshot execution inside Memgraph)

### Perform backup

Backup the snapshot for every database into a 3rd party location. Currently, you’re encouraged to perform the backup mechanisms by yourself with tools such as [rclone](https://rclone.org/).

### When performing recovery, copy the snapshot to Memgraph

When recovering a specific database, copy the snapshot to any data location

- if the data directory the snapshot is being copied to is a location that’s outside the database directory, ensure the snapshot has the permissions to be copied to the database data directory
- if the data directory the snapshot is being copied to is a location that’s inside the database directory, there should be no issues with permissions as there is no copying being performed from source to target directory location

### Position to specific database

Position the database driver interacting with Memgraph into the database using `USE DATABASE <database_name>`

### Recover the snapshot

Execute `RECOVER SNAPSHOT <path_to_snapshot> FORCE`

## Usage of .old directory[](https://memgraph.com/docs/database-management/backup-and-restore#usage-of-old-directory)

By default, Memgraph backs up durability files to `snapshots/.old` and `wal/.old` directories before operations that could risk data loss.

When backup occurs:

1. `RECOVER SNAPSHOT` query - Before loading an external snapshot, Memgraph moves existing files from `snapshots/` to `snapshots/.old` and from `wal/` to `wal/.old`. T his protects your data if the newly loaded snapshot turns out to be corrupted.
2. High Availability force sync - During replica’s force syncing. See [this page](https://memgraph.com/docs/clustering/high-availability/how-high-availability-works#replication-scenarios) for details.

Configuration:

Use the `--storage-enable-backup-dir` flag to control this behavior:

- `true` (default) - Old durability files are moved to `.old` directories
- `false` - Old durability files are deleted immediately

## Best practices[](https://memgraph.com/docs/database-management/backup-and-restore#best-practices)

Memgraph can optimize restoring of snapshots in a multi-threaded manner. To enable multi-threaded restoration of a snapshot, you need to ensure the following flags are present:

- `--storage-parallel-schema-recovery=true`
- `--storage-recovery-thread-count=<number_of_cores>` where `number_of_cores` is the amount of CPU cores to parallelize the restoration process
