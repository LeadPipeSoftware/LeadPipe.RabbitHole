![Lead Pipe Software Logo](LeadPipeSoftwareLogoColor.png)

# LeadPipe RabbitHole

RabbitHole is a RabbitMQ message utility. It can:

* Save messages in a queue to a JSON file (snag)
* Send messages in a JSON file to a queue (queue)
* Re-queue messages in one queue to another (replay)

## Example Usage

### Queue Messages From JSON

```bash
$ rabbithole queue -d MyRabbitQueue -f message_to_queue.json
```

### Save Messages as JSON

```bash
$ rabbithole snag -q error -m 1 -a snagged_errors.json
```

### Replay Messages

```bash
$ rabbithole replay -q error -m 1 -d MyRabbitQueue
```

[Lead Pipe Software](http://www.leadpipesoftware.com)
