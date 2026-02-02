### Strategic analysis agent

An agent that can search for a strategic analysis for any pokemon/generation/tier on Smogon Academy (or a similar website).

The result depends on what's requested by the AI. The input is a phrase, not a structured query, and the output is the same.

Testing must be done to ensure that this is working as expected, and also to determine if it's fast enough.

### Strategic dictionnary agent

An agent that can give definitions for strategic terms used in competitive Pokemon.

As an input, you give it a string, and you receive a precise definition of this term as an output. This can either be achieved by searching in a list with some leiniency, or by using an AI to detect what word was requested.

When the term is not found, the agent should return a specific message/value indicating that the term is not in the dictionnary.