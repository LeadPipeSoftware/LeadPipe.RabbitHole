.. _`User Guide`:

User Guide
============

Snag
-------------------------------------------------------

Save a copy of messages in a queue as a JSON file.

Sometimes you want to save a copy of a message in a queue. Hey, you might even want to save the whole queue! That's where the snag command comes in handy.

.. code-block:: bash

    $ ./rabbithole.exe snag -q MyRabbitQueue -m 1 -a snagged.json


Queue
------------------------------------------------

Send messages to a queue from a JSON file.

What about the other way around? Let's say you want to publish a message using a JSON-formatted source file. That's where the queue command steps in.

.. code-block:: bash

    $ ./rabbithole.exe queue -d MyRabbitQueue -f snagged.json

You can specify a JSON file with a single message, a JSON file containing an array of multiple messages, or a folder containing JSON files.

Shuttle
----------------------------------------------------------------

Get messages from a queue and put them on another queue.

Need to move messages from one queue to another? The shuttle command has you covered.

.. code-block:: bash

    $ ./rabbithole.exe shuttle -q FooQueue -d BarQueue -m 5

You can shuttle a single message or as many messages as you'd like!

Replay
---------------------------------------------

Return messages to their source queue.

What about simply re-playing a message by returning it to its source queue? Fire up the handy replay command!

.. code-block:: bash

    $ ./rabbithole.exe replay -q FooQueue -m 5

You can replay a single message or as many messages as you'd like!

Configuration
-------------

RabbitHole is a command-line tool and almost every option can be specified as an argument. To see what you can do, just ask!

.. code-block:: bash

    $ ./rabbithole.exe -h

To get help with a specific command simply supply the command name like this:

.. code-block:: bash

    $ ./rabbithole.exe replay -h

In addition, RabbitHole supports the (optional, but installed by default) use of a configuration file. Here's an example (tweaked for NServiceBus).

.. code-block:: ini

    [General]
    Simulate=False
    MaxThreads=1000
    ;;; The Verbose, Silent, and Debug options are mutually exclusive - set ONE of them True or ALL of them False
    Verbose=False
    Silent=False
    Debug=False

    [Messages]
    SourceQueueFields=NServiceBus.FailedQ,NServiceBus.ProcessingEndpoint
    FieldsToRemove=NServiceBus.FLRetries,NServiceBus.Retries,$.diagnostics.originating.hostid,$.diagnostics.hostdisplayname,$.diagnostics.hostid,$.diagnostics.license.expired,NServiceBus.Version,NServiceBus.TimeSent,NServiceBus.EnclosedMessageTypes,NServiceBus.ProcessingStarted,NServiceBus.ProcessingEnded,NServiceBus.OriginatingAddress,NServiceBus.ProcessingEndpoint,NServiceBus.ProcessingMachine,NServiceBus.FailedQ

    [RabbitMQ]
    HostUrl=http://localhost
    HostPort=15672
    VHost=%2F
    Username=guest
    ;;; Putting the password in a plain text file is a TERRIBLE idea, but if you insist...
    Password=guest

