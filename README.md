# RocketPod base frontend package

This is the basic setup for all frontend work at RocketPod. This is a bare-bones
build system and each project will likely need its own amendments and additions.

Currently built on top of the [Concise framework](http://concisecss.com/documentation/layout/container/)

## Quick start

Clone the repository:

`git clone git@bitbucket.org:rocketpod/rocketpod-foundation.git`

Install development dependencies:

`npm install`

Install frontend dependencies:

`bower install`

Build the static files

`gulp`

Start watching for changed to SCSS and JS:

`gulp watch`

This session needs to stay open to process the SCSS & JS files.

### Development

**Javascript** development is vanilla at the moment. Might move to something
else soon.

**CSS** development is using SCSS. Style files should be modularised where
necessary/sensible.

To do this, create an underscore (`_`) prefixed file, and
import it in the `main.scss` file. SCSS imports are ordered, so base styles
should be at the top.

**Concise** modules are imported via `src/scss/_framework.scss` as needed.

### Extending the build system

The build system uses [gulp](http://gulpjs.com/) to run tasks. You can see the
functions which make up the workflow in `Gulpfile.js`.
You can add/remove/modify these in your project.

