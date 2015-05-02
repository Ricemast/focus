# Focus

**Focus** is a tool to help you get things done.

Currently it is a simple, opinionated task list. Soon **Focus** will be
a fully featured, modular, type based productivity multitool.

## Installation

**Focus** is a simple django application configured to run on SQLite3.

Simply clone this repository, `cd` to the `focus` django application directory
and setup the DB using:

`./manage.py syncdb`

`./manage.py migrate`

Then create an admin account so you can login to the django admin panel
(`/admin`)

`./manage.py createsuperuser`

The development tools are managed through [npm](https://www.npmjs.com/).

Install the *npm* packages with `npm install`

Frontend dependencies are managed with [bower](http://bower.io/).

Install the *bower* packages with `bower install`

The static assests are built using [gulp](http://gulpjs.com/).

Build the assests with `gulp`

Build and watch the assests with `gulp watch`

### Development

*Javascript* development is vanilla at the moment. Might move to something
else soon.

*CSS* development is using SCSS. Style files should be modularised where
necessary/sensible. I'm not following any particular style guide at the moment.
I might migrate the code to something while the codebase is small.

[Concise](http://concisecss.com/documentation/) modules are imported in
`src/scss/_framework.scss` as needed.

## Usage

TODO: Write usage instructions

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b feature/my-new-feature`
3. Commit your changes: `git commit -am 'Added some feature'`
4. Push to the branch: `git push origin feature/my-new-feature`
5. Submit a pull request :D

## History

- **Version 0.1**: Basic sequential todo list. Tests and readme written.

## Credits

Alex Price ([@ricemast](https://twitter.com/ricemast))

## License

The MIT License (MIT)

Copyright (c) 2015 Alex Price

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
