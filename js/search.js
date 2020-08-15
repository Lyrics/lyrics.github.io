var baseURL = 'https://api.github.com/repos/Lyrics/lyrics/contents/database/'
var searchBaseURL = 'https://api.github.com/search/code?q=repo:Lyrics/lyrics path:database/ fork:false '
var debounceTime = 1000
var dbPrefix = '/db'

function formatURL (input) {
    input = encodeURI(input).replace(/\?/g, '%3F')
    return dbPrefix + input + '/'
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
                    var reason = response.status == 403 ?
                        'Search API rate limit exceeded, please try searching again later' :
                        'Something went wrong'
                    cb(new Error(reason))
                })
        }
    }
}

var Search = {
    data: function () {
        return {
            init: true,
            loading: false,
            error: null,
            items: null
        }
    },
    created: function () {
        setTimeout(function () {
            document.getElementsByTagName('input')[0].value = this.$route.query.q
        }.bind(this))
        this.fetchData()
    },
    mounted: function () {
        this.$el.className = 'search'
    },
    watch: {
        '$route': 'fetchData'
    },
    methods: {
        fetchData: debounce(function () {
            this.init = false
            this.loading = true
            this.error = this.items = null

            API.search(this.$route.query.q, function (err, items) {
                this.loading = false

                if (err) {
                    this.error = err.toString()
                } else if (items.length) {
                    this.items = items
                }
            }.bind(this))
        }, debounceTime)
    },
    template: '<div>' +
                '<div class="loading" v-if="loading">Loading…</div>' +
                '<div v-if="error" class="error">{{ error }}</div>' +
                '<div v-if="items" class="content">' +
                  '<ul id="l">' +
                    '<li v-for="item in items"><a class="t3" :href="formatURL(item.path.substring(8))">{{ item.path.split("/")[2] }} – {{ item.name }}</a></li>' +
                  '</ul>' +
                '</div>' +
                '<div v-if="!init && !loading && !error && !items" class="content">' +
                  '<p>No results</p>' +
                '</div>' +
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
