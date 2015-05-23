# Focus

**Focus** is a personal project to help me get things done.

Currently it is a simple, opinionated todo list. Soon **Focus** will be
a fully featured, modular, type based productivity multitool.

## Installation

**Focus**'s backend is a simple django application with a
django-rest-framework API. It is configured to run on mysql (you may
need to change the db settings in `focus/settings.py`). The frontend is an
[Aurelia](http://aurelia.io/) application. Aurelia is a JavaScript client
framework build on next gen JS (ES6-7).

To get up and running simply clone this repository, and setup the DB using:

`./manage.py syncdb`

`./manage.py migrate`

The development tools are managed through [npm](https://www.npmjs.com/).

Install the *npm* packages with `npm install`

Frontend dependencies are managed with [jspm](http://jspm.io/).

Install the *bower* packages with `jspm install -y`

The static assests are built using [gulp](http://gulpjs.com/).

Build and watch the assests with `gulp watch`

You need to have both the API server and the frontend server running to view
**Focus**. `gulp watch` should handle serving the frontend. You will need to
run `./manage.py runserver` to start the django server.

Browse to [http://localhost:9000](http://localhost:9000) to see the app.

### Development

*Django* development is split into **applications**. Currently the base
application is `focus`. This holds the settings etc. Models and API views are
in the `todos` application.

*JavaScript* development is in ES6-7. You can learn about it
[here](https://babeljs.io/docs/learn-es6/). The frontend files are found in the
`src` directory. The browser should auto-refresh as you save files (you may
need the [live-reload](http://livereload.com/) browser plugin).

*CSS* development is using SCSS. Style files should be modularised where
necessary/sensible. I'm not following any particular style guide at the moment.
I might migrate the code to something while the codebase is small.

[Concise](http://concisecss.com/documentation/) modules are imported in
`frontend/scss/_framework.scss` as needed.

## Usage

TODO: Write usage instructions

## Testing

*Django* tests are run using `./manage.py test`

*Aurelia* test are yet to be written.

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b feature/my-new-feature`
3. Commit your changes: `git commit -am 'Added some feature'`
4. Push to the branch: `git push origin feature/my-new-feature`
5. Submit a pull request :D

## History

- **Version 0.1**: Basic sequential todo list. Tests and readme written.
- **Version 0.2**: Conversion of frontend to use the Aurelia framework.
- **Version 0.3**: Added CRUD.

## Credits

**Focus** was created by Alex Price ([@ricemast](https://twitter.com/ricemast))

## License

The MIT License (MIT)

Copyright (c) 2015 Focus

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
