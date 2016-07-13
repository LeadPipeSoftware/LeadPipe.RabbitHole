Feature: Save a copy of messages in a queue to a file
  In order to work with a message
  As a user
  I want to save RabbitMQ messages to a file

  Background: A RabbitMQ host exists with at least one message
    Given a RabbitMQ host
    And a queue named "Test"

  Scenario: Save one message
    Given a message exists in the source queue
    When I
    Then