# Controllers Explanation

Ideally on a big and scalable project the software must be implemented with some kind of architecture that focus on responsibility segregation, like Clean Architecture or Hexagonal Architecture.

In this project, for the sake of simplicity and due to time constraints, the `Controller` pattern will assume the responsibility of the Clean Architecture's Use Case (and it's DTOs) by being the interface between the REST API and the `Repository` pattern.