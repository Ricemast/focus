export class App {
    configureRouter(config, router){
        this.router = router;

        config.title = 'Focus';
        config.map([
            {
                route: '',
                moduleId: './pages/todos',
                title: 'Home'
            },
            {
                route: 'focus/:id',
                moduleId: './pages/focus',
                title: 'Focus'
            }
        ]);

    }
}
