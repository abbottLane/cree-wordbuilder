import { Subject, Observable } from 'rxjs'

export enum Status {
    disconnected = 0,
    connecting,
    waiting,
    connected,
    error,
    failed
}

export interface Payload {
    type: string
    data: SearchResults | number | DictResults
} 

export interface SearchResults {
    results: string[]
    total: number
}

export interface DictResults {
    analysis: string[]
    dictresults: string[]
    total: number
}

export class Backend {
    private url: string
    private websocket: WebSocket
    private messages: Subject<Payload> = new Subject()
    private timeout: number = null
    private retries: number = 0
    constructor(backendurl: string) {
        this.url = backendurl
    }

    connect() {
        
        if (this.websocket) {
            console.log('existing web socket, status', this.websocket.readyState)
            if (this.websocket.readyState === WebSocket.CONNECTING) {
                console.log('web socket was already trying to connect, closing it')
                this.websocket.close()
            }
        }
        this._startWebsocket()
    }

    _startWebsocket() {
        const reconnect = () => {
            this.messages.next({type: 'status', data: Status.waiting})
            setTimeout(() => {
                this._startWebsocket()
            }, 10000)
        }
        console.log('opening websocket')
        this.messages.next({type: 'status', data: Status.connecting})
        this.websocket = new WebSocket(this.url)
        this.websocket.onmessage = (msg) => {
            const j = JSON.parse(msg.data)
            if (j.type === 'pong') {
                console.log('pong')
            } else {
                this.messages.next(j)
            }
        }
        this.websocket.onopen = () => {
            this.messages.next({type: 'status', data: Status.connected})
            this.retries = 0
            this._keepalive()
        }
        // turns out it fires this AND the onclose event
        this.websocket.onerror = (e) => {
            this.messages.next({type: 'status', data: Status.error})
            console.log('onerror fired', e.type)
        }
        this.websocket.onclose = (e) => {
            console.log('onclosefired', e.code)
            this._clearTimeout()
            if (e.code === 1000) {
                // normal close
            } else {
                this.messages.next({type: 'status', data: Status.disconnected})
                ++this.retries
                if (this.retries < 10) {
                    reconnect()
                } else {
                    this.messages.next({type: 'status', data: Status.failed})
                }
            }
        } 
    }

    close() {
        if (this.isOpen()) {
            this.websocket.close()
        }
    }

    observe(): Observable<Payload> {
        return this.messages.asObservable()
    }

    sendMessage(pl: Payload) {
        if (this.isOpen()) {
            this.websocket.send(JSON.stringify(pl))
        } else {
            throw new Error('websocket not connected')
        }
    }

    isOpen() {
        return this.websocket.readyState === WebSocket.OPEN
    }

    search(sstring: string, limit: number) {
        if (this.isOpen()) {
            const sparms = {
                search: sstring,
                limit: limit
            }
            this.websocket.send(JSON.stringify({ type: 'search', data: sparms}))
        }
    }
    dict_search(sstring: string) {
        if (this.isOpen()) {
            const sparms = {
                dictsearch: sstring,
            }
            this.websocket.send(JSON.stringify({ type: 'dictsearch', data: sparms}))
        }
    }
    _clearTimeout() {
        if (this.timeout) {
            clearTimeout(this.timeout)
            this.timeout = null
        }
    }

    _keepalive() {
        this.timeout = window.setTimeout(() => {
            if (this.isOpen()) {
                console.log('ping')
                this.websocket.send(JSON.stringify({ type: 'ping' }))
                this._keepalive()
            }
        }, 10000)
    }

}
