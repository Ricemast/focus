export class App {
    configureRouter(config, router){
        config.title = 'Focus';

        config.map([
            {
                route: ['','todos'],
                moduleId: './pages/todos',
                title:'Todos'
            }
        ]);

        this.router = router;
    }
}
