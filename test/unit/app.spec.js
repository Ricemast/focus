import {App} from '../../src/app';

class RouterStub {
  configure(handler) {
    handler(this);
  }
  map(routes) {
    this.routes = routes;
  }
}

describe('the App module', () => {
  var sut, mockedRouter;

  beforeEach(() => {
    mockedRouter = new RouterStub();
    sut = new App(mockedRouter);
    sut.configureRouter(mockedRouter, mockedRouter);
  });

  it('contains a router property', () => {
    expect(sut.router).toBeDefined();
  });

  it('configures the router title', () => {
    expect(sut.router.title).toEqual('Focus');
  });

  it('should have a home route', () => {
    expect(sut.router.routes).toContain({ route: '',  moduleId: './pages/todos', title: 'Home' });
  });

  it('should have a focus route', () => {
     expect(sut.router.routes).toContain({ route: 'focus/:id', moduleId: './pages/focus', title: 'Focus' });
  });

});
