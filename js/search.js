'use strict'


var baseURL = 'https://api.github.com/repos/Lyrics/lyrics/contents/database/'
var searchBaseURL = 'https://api.github.com/search/code?q=repo:Lyrics/lyrics path:database/ fork:false '
var debounceTime = 1000
var dbPrefix = '/db'


function formatURL (input) {
    if (input)
        return dbPrefix + encodeURI( input.replace(/ /g, '-').toLowerCase() ).replace(/\?/g, '%3F') + '/'
}


/* API */

var API = {
    search: function (query, cb) {
        if (query.length < 3) {
            cb(new Error("Query too short"))
        } else {
            Vue.http.get(searchBaseURL + query).then(
                function (response) {
                    cb(null, response.body.items)
                },
                function (response) {
                    var reason = response.status == 403 ? 'Search API rate limit exceeded, please try searching again later' : 'Something went wrong'
                    cb(new Error(reason))
                })
        }
    }
};

var Search = {
    data: function () {
        return {
            loading: false,
            items: null,
            error: null
        }
    },
    created: function () {
        document.getElementById('query').value = this.$route.query.q
        this.fetchData()
    },
    watch: {
        '$route': 'fetchData'
    },
    methods: {
        fetchData: debounce(function () {
            this.error = this.items = null
            this.loading = true

            API.search(this.$route.query.q, function (err, items) {
                this.loading = false

                if (err) {
                    this.error = err.toString()
                } else {
                    this.items = items
                }
            }.bind(this))
        }, debounceTime)
    },
    template: '<div class="search">' +
                '<div class="loading" v-if="loading">Loading…</div>' +
                '<div v-if="error" class="error">{{ error }}</div>' +
                '<transition name="slide">' +
                 '<div v-if="items" class="content">' +
                  '<ul id="ls">' +
                   '<li v-for="item in items"><a :href="formatURL(item.path.substring(8))">{{ item.path.split("/")[2] }} – {{ item.name }}</a></li>' +
                  '</ul>' +
                 '</div>' +
                '</transition>' +
                '</div>'
}


/* Set up the routing */

Vue.use(VueRouter)

var router = new VueRouter({
    mode: 'history',
    routes: [
        {
            path: '/search.html',
            component: Search
        }
    ]
})


/* Initiate the framework */

new Vue({
    router: router,
    data: { }
}).$mount('#app')
