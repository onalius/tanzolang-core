# TanzoLang: The Tomodaichi Tanzo Specification

Welcome to the TanzoLang documentation. TanzoLang is a schema language for defining digital archetypes and attributes in the Tomodaichi Tanzo ecosystem.

## What is TanzoLang?

TanzoLang is a JSON-Schema based specification that allows you to define profiles containing digital archetypes with various attributes. These attributes can have fixed values or probability distributions, enabling Monte-Carlo simulations and other probabilistic analyses.

## Features

- **Flexible Schema**: Define digital, physical, and hybrid archetypes with arbitrary attributes
- **Probability Distributions**: Support for normal, uniform, and discrete probability distributions
- **Validation**: Ensure your profiles conform to the TanzoLang specification
- **Simulation**: Run Monte-Carlo simulations to explore the probability space of your profiles
- **Export**: Convert profiles to concise string representations for sharing and display

## Quick Start

### Install the Python SDK

```bash
pip install tanzo-schema
