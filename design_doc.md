 # Design Doc

## Overview

This app is an email classifier that automatically categorizes incoming emails into various categories that we have outlined  
in our datasets from the labs.

We're using multiple different machine learning classifiers like `logistic regression` and `gradient boosting` to classify  
our emails.

## Breakdown

### Factory Pattern

#### Justification

A Factory pattern allows for easy scalability within our App as we can easily scale out as it allows us to implement a  
variety of factories that produce different models for us and the client to use.

The overall design goal for this model is to make the app more scalable, configurable and flexible as it allows the user  
to directly interact with the model-making process of the app.

![Factory Pattern](./images/Factory_Diagram.png)

> Abstract Base Classes were used to prevent instantiation of base classes and interfaces for good code health.

### Decorator Pattern

#### Justification

We decided to use a Decorator pattern to help create interfaces that allows us to create multiple interfaces that can be  
extended to fit a variety of purposes as there are multiple ways to handle creating, loading, processing, and translating data.  
This allows for more flexibility within our app, we need to allow our app to fit a variety of purposes.

This is a slightly tweaked implementation of a Decorator pattern as Python has a few issues with properly implementing a decorator
class, we have instead a function that acts as a decorator, which in our case is ``autoprocessed(func)``.

![Decorator Pattern](./images/Decorator_Diagram.png)

### Singleton

#### Justification

The Singleton Util class provides a method to allow all other classes within our app to access the project directory, as  
that's required by most if not all of our classes within our implementation.

The purpose of this pattern is to allow maintainability within our app.

![Singleton](./images/Singleton.png)

### Facade

#### Justification

We went for making a Facade class to act as a body that our clients can query to handle the various ways our Factory pattern  
had handled making models as we are taking care of our clients wanting to use different datasets and having to tweak the  
products that our Factory pattern had made.

To do achieve this pattern we turned our Factory Pattern into a series of subsystem classes that link to the main Facade  
class.

The primary goal of this Facade pattern was to help us achieve flexibility and scalability within our app, as when our  
app requires more functionality this pattern is able to handle new additions to our app.

![Facade](./images/Facade_Diagram.png)

### Strategy

#### Justification

One of our goals was to have a CLI that our users can interact with, thus we decided to use a Strategy pattern to encapsulate  
the more complex parts of our app into a more client-friendly interface.

Our Strategy pattern is in the form of a CLI, where we have encapsulated the behaviour of our datasets and Facade into a
usable form for our clients.

The main goal of this pattern was to make our app more flexible, as it allows us to have a mechanism to encapsulate and interchange  
algorithms at runtime.

![Strategy](./images/Strategy_Diagram.png)

### Sequence Diagram

The below diagram outlines the flow of events as a user interacts with our app. We primarily make things go through the CLI  
as it's the main way that the user interacts with the app.

![Sequence of events](./images/Sequence_Diagram.png)

