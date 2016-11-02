'use strict'


var baseURL = 'https://api.github.com/repos/Lyrics/lyrics/contents/database/'
var searchBaseURL = 'https://api.github.com/search/code?q=repo:Lyrics/lyrics path:database/ fork:false '
var debounceTime = 1000;
var dbPrefix = '/db';


function escapeURLChars (input) {
    console.log(input)
    if (input)
        return input.replace(/\?/g, '%3F');
}


/* API */

function APIreadPath (path, cb) {
    Vue.http.get(baseURL + path).then(
        function(response) {
            if (response.ok) {
                cb(null, response.body)
            } else {
                cb(new Error('Empty directory'))
            }
        },
        function(response) {
            var reason = response.status == 403 ? 'API rate limit exceeded, please wait a bit before trying again' : 'Something went wrong'
            cb(new Error(reason))
        })
}

function APIreadFile (path, cb) {
    Vue.http.get(baseURL + path).then(
        function(response) {
            Vue.http.get(response.body.download_url).then(
                function (response) {
                    cb(null, response.body)
                },
                function (response) {
                    cb(new Error("Something went wrong again"))
                })
        },
        function(response) {
            var reason = response.status == 403 ? 'API rate limit exceeded, please wait a bit before trying again' : 'Something went wrong'
            cb(new Error(reason))
        })
}

function APIsearch (query, cb) {
    if (query.length < 3) {
        cb(new Error("Query too short"))
    } else {
        Vue.http.get(searchBaseURL + query)
            .then(function (response) {
                cb(null, response.body.items)
            },
            function (response) {
                var reason = response.status == 403 ? 'Search API rate limit exceeded, please try searching again later' : 'Something went wrong'
                cb(new Error(reason))
            })
    }
}


/* Breadcrumbs */

var breadcrumbsData = []

function updateBreadcrumbs(route) {
    if (breadcrumbsData.length) {
        for (var i = breadcrumbsData.length; i >= 0; i--)
            Vue.delete(breadcrumbsData, i)
    }

    if (!route) return;

    var usedParams = [];
    var i = 1;
    for (var pname in route.params) {
        if (!route.params[pname]) continue;

        var path = (dbPrefix + '/' + usedParams.join('/') + '/' + route.params[pname]).replace(/\/+/g, '/')
        Vue.set(breadcrumbsData, i++, { path: path, name: route.params[pname] })
        usedParams.push(route.params[pname])
    }
}


/* / */

var Home = {
    created: function () {
        document.title = 'Lyrics'
        updateBreadcrumbs()
    },
    template: '<div>Please start by picking a letter or using the search field</div>'
}


/* /db/:letter/:artist/:album */

var Path = {
    data: function () {
        return {
            loading: false,
            items: null,
            error: null
        }
    },
    created: function () {
        this.fetchData()
    },
    watch: {
        '$route': 'fetchData'
    },
    methods: {
        fetchData: function () {
            this.error = this.items = null
            this.loading = true

            APIreadPath([
                this.$route.params.letter,
                escapeURLChars(this.$route.params.artist),
                escapeURLChars(this.$route.params.album)
            ].join('/').replace(/\/*$/, ''), function (err, items) {
                this.loading = false
console.log(items)
                if (err) {
                    this.error = err.toString()
                } else {
                    this.items = items
                }

                var title = []

                if (this.$route.params.album)
                    title.push(this.$route.params.album)
                if (this.$route.params.artist)
                    title.push(this.$route.params.artist)
                if (this.$route.params.letter)
                    title.push(this.$route.params.letter)

                title.push('Lyrics')

                document.title = title.join(' | ')

                updateBreadcrumbs(this.$route)
            }.bind(this))
        }
    },
    template: '<div class="path">' +
                '<div class="loading" v-if="loading">Loading…</div>' +
                '<div v-if="error" class="error">{{ error }}</div>' +
                '<transition name="slide">' +
                 '<div v-if="items" class="content">' +
                  '<ul id="ls">' +
                   '<li v-for="item in items"><router-link :to="{ path: escapeURLChars(item.name) }" append>{{ item.name }}</a></li>' +
                  '</ul>' +
                 '</div>' +
                '</transition>' +
                '</div>'
}


/* /db/:letter/:artist/:album/:song */

var File = {
    data: function () {
        return {
            loading: false,
            text: null,
            error: null
        }
    },
    created: function () {
        this.fetchData()
    },
    watch: {
        '$route': 'fetchData'
    },
    methods: {
        fetchData: function () {
            this.error = this.text = null
            this.loading = true

            APIreadFile([
                this.$route.params.letter,
                escapeURLChars(this.$route.params.artist),
                escapeURLChars(this.$route.params.album),
                escapeURLChars(this.$route.params.song)
            ].join('/').replace(/\/*$/, ''), function (err, text) {
                this.loading = false

                if (err) {
                    this.error = err.toString()
                } else {
                    this.text = text
                }

                document.title = this.$route.params.artist + ' – ' + this.$route.params.song + ' |  Lyrics'

                updateBreadcrumbs(this.$route)
            }.bind(this))
        }
    },
    template: '<div class="file">' +
                 '<div class="loading" v-if="loading">Loading…</div>' +
                 '<div v-if="error" class="error">{{ error }}</div>' +
                 '<transition name="slide">' +
                  '<div v-if="text" class="content"><pre>{{ text }}</pre></div>' +
                 '</transition>' +
               '</div>'
}


Vue.component('search-query', {
    data: function () {
        return {
            query: '',
        }
    },
    methods: {
        find: function () {
            if (this.query.length) {
                this.$router.push('/search/' + this.query)
            }
        }
    },
    template: '<input id="query" type="search" v-on:input="find" v-model="query" placeholder="Search" />'
})

var Search = {
    data: function () {
        return {
            loading: false,
            items: null,
            error: null
        }
    },
    created: function () {
        document.title = 'Search | Lyrics'
        updateBreadcrumbs()
        this.fetchData()
    },
    watch: {
        '$route': 'fetchData'
    },
    methods: {
        fetchData: debounce(function () {
            this.error = this.items = null
            this.loading = true

            APIsearch(this.$route.params.query, function (err, items) {
                this.loading = false

                if (err) {
                    this.error = err.toString()
                } else {
                    this.items = items
                }
                console.log(items)
            }.bind(this))
        }, debounceTime)
    },
    template: '<div class="search">' +
                '<div class="loading" v-if="loading">Loading…</div>' +
                '<div v-if="error" class="error">{{ error }}</div>' +
                '<transition name="slide">' +
                 '<div v-if="items" class="content">' +
                  '<ul id="ls">' +
                   '<li v-for="item in items"><router-link :to="{ path: dbPrefix + item.path.substring(8) }">{{ item.path.split("/")[2] }} – {{ item.name }}</a></li>' +
                  '</ul>' +
                 '</div>' +
                '</transition>' +
                '</div>'
}


/* Set up the routing */

Vue.use(VueRouter)

var router = new VueRouter({
    mode: 'history',
    linkActiveClass: 'active',
    routes: [
        {
            path: '/',
            component: Home
        },
        {
            path: dbPrefix + '/:letter/:artist?/:album?',
            component: Path
        },
        {
            path: dbPrefix + '/:letter/:artist/:album/:song',
            component: File
        },
        {
            path: '/search/:query',
            component: Search
        }
    ]
})


/* Initiate the framework */

new Vue({
    router: router,
    data: function () {
        return {
            alphabet: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split(''),
            breadcrumbs: breadcrumbsData
        }
    }
}).$mount('#app')
