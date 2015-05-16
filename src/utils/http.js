/*jshint esnext:true */
import {HttpClient} from 'aurelia-http-client';
import {vars} from '../utils/variables';

export let http = new HttpClient().configure(x => {
    x.withBaseUrl(vars.backend_url);
    x.withHeader('Content-Type', 'application/json');
});
