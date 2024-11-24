 # Design Doc

## Overview

This app is an email classifier that automatically categorizes incoming emails into various categories that we have outlined  
in our datasets from the labs.

We're using multiple different machine learning classifiers like `logistic regression` and `gradient boosting` to classify  
our emails.

## Breakdown

### Factory Pattern

We're using a Factory pattern to provide machine learning models to the user that the app uses.

![Factory Pattern](./images/Factory_Diagram.png)

### Decorator Pattern

This is a slightly tweaked version of a Decorator pattern as Python has a few issues with properly implementing a decorator
class, we have instead a function that acts as a decorator, which in our case is ``autoprocessed(func)``.

![Decorator Pattern](./images/Decorator_Diagram.png)

### Singleton

Our Singleton Util class provides a method to allow all other classes within our app to access the project directory, as
outlined in the UML diagram.

![Singleton](./images/Singleton.png)

### Facade

We use a Facade pattern for our client interface, which provides methods that are in the subsystem classes in one class that
the users can access.

![Facade](./images/Facade_Diagram.png)

### Strategy

Our Strategy pattern is in the form of a CLI, where we have encapsulated the behaviour of our datasets and Facade into a
usable form for our clients.

![Strategy](./images/Strategy_Diagram.png)

### Sequence Diagram

The below diagram outlines the flow of events as a user interacts with our app.

![Sequence of events](./images/Sequence_Diagram.png)

