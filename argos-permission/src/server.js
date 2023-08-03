'use strict';

function metricsContain(metric) {
    return metrics.some((obj) => obj.name === metric.name);
};

const Hapi = require('@hapi/hapi');
const Server = Hapi.Server({
    host: '0.0.0.0',
    port: 3000
});

const metrics = [];

Server.route({
    method: 'GET',
    path: '/api/metric',
    handler: (request) => {
        return metrics;
    }
});

Server.route({
    method: 'GET',
    path: '/api/metric/{name}',
    handler: (request, _h) => {
        const metric = metrics.filter((metric) => metric.name === request.params.name);
        return { found: Boolean(metric.length), metric: metric }
    }
});

Server.route({
    method: 'POST',
    path: '/api/metric',
    handler: (request, h) => {
        const metric = request.payload;
        if (!metricsContain(metric)) {
            metrics.push({
                name: metric.name,
                start: Number(metric.start),
                end: Number(metric.end),
                permission: true
            });
            return { created: true, path: `/api/unsubscribe/${metric.name}` };
        };
        return { created: false, path: '' };
    }
});

Server.route({
    method: 'POST',
    path: '/api/metric/bulk',
    handler: (request, h) => {
        request.payload.forEach(metric => {
            if (!metricsContain(metric)) {
                metrics.push({
                    name: metric.name,
                    start: Number(metric.start),
                    end: Number(metric.end),
                    permission: true
                });
            };
        });
        return metrics;
    }
});

Server.route({
    method: 'GET',
    path: '/api/permission',
    handler: (request, h) => {
        const metric = metrics.find((metric) => metric.name === request.query.name);
        let permission = false;
        let path = '';

        if (typeof metric !== 'undefined') {
            if (request.query.start > metric.end) {
                metric.start = Number(request.query.start);
                metric.end = Number(request.query.end);
                metric.permission = true;

                if (metric.permission) {
                    path = `/api/unsubscribe/${metric.name}`;
                };

                permission = metric.permission
            };
        };
        return { permission: permission, path: path };
    }
});

Server.route({
    method: 'GET',
    path: '/api/subscribe/{name}',
    handler: (request, h) => {
        const metric = metrics.find((metric) => metric.name === request.params.name);

        metric.permission = true;

        return 'You will receive notification from this metric.';
    }
});

Server.route({
    method: 'GET',
    path: '/api/unsubscribe/{name}',
    handler: (request, h) => {
        const metric = metrics.find((metric) => metric.name === request.params.name);

        metric.permission = false;

        return 'You will no longer receive notification from this metric.';
    }
});

Server.events.on('response', (request) => {
    console.log(`${request.info.remoteAddress}> ${request.method.toUpperCase()} ${request.url.pathname} --> ${request.response.statusCode}`);
});

(async () => {
    try {
        const options = {
            ops: {
                interval: 1000
            },
            reporters: {
                file: [{
                    module: 'good-squeeze',
                    name: 'Squeeze',
                    args: [{
                        log: '*',
                        response: '*'
                    }]
                }, {
                    module: 'good-squeeze',
                    name: 'SafeJson'
                }, {
                    module: 'good-file',
                    args: ['./logs/server.log']
                }]
            }
        };

        await Server.register({
            plugin: require('good'),
            options
        })

        await Server.start();

        console.log(`Server running at: ${Server.info.uri}`);
    } catch (err) {
        console.log(err);
    };
})();
