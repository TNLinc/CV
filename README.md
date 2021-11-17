# CV service

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/3f272df9d9be4a948ce9f0a00a4dc343)](https://www.codacy.com/gh/TNLinc/CV/dashboard?utm_source=github.com&utm_medium=referral&utm_content=TNLinc/CV&utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/TNLinc/CV/branch/main/graph/badge.svg?token=FORLTJT0TH)](https://codecov.io/gh/TNLinc/CV)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![CodeFactor](https://www.codefactor.io/repository/github/tnlinc/cv/badge)](https://www.codefactor.io/repository/github/tnlinc/cv)

We decided to use Flask for a CV service because it is lightweight and synchronous (CV is a cpu-bound task).

Service logic now use [Fabric](https://refactoring.guru/ru/design-patterns/factory-method) pattern and [Cain of responsibility](https://refactoring.guru/ru/design-patterns/chain-of-responsibility) pattern.

We add swagger to have easy access to the routes. Now this service only has one route, which takes an image and return color of face skin (using OpenCV [see](https://github.com/KochankovID/TonalCreamAssistant/wiki/Face-recognition)).
