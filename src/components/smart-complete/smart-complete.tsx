import { Component, Prop, State, h } from '@stencil/core';
import { throttle } from 'throttle-debounce';
import { Backend, Status, SearchResults, DictResults } from './backend'
// import logo from './logo.svg';


@Component({
    tag: 'smart-complete',
    styleUrl: 'smart-complete.scss',
    shadow: true
})
export class SmartComplete {
    @Prop() backend: string
    @Prop() throttle: number = 600
    @Prop() limit: number = 10
    @State() searchresults: SearchResults = {results: [], total: 0}
    @State() dictionaryresults: DictResults = {analysis: [], dictresults: [], total: 0}
    @State() status: Status = Status.disconnected
    lastPress: number
    wantUpdate: false
    textInput: HTMLInputElement;
    currentWord: string;
    throttled: Function = throttle(this.throttle, false, this.throttledChanged)
    //data: Backend = new Backend('wss://kunwok-service.herokuapp.com/ws')
    data: Backend = new Backend('ws://localhost:8000/ws')

    handleSubmit(e) {
        e.preventDefault()
        console.log(this.textInput.value);
        // send data to our backend
        const val = this.textInput.value // make a copy of it
        this.data.dict_search(val)
      }

    async componentWillLoad() {
        this.data.observe().subscribe((data) => {
            if (data.type === 'status') {
                this.status = data.data as number
                if (this.status === Status.connected) {
                    console.log('connected')
                }
            } else if (data.type === 'results') {
                this.searchresults = data.data as SearchResults
                console.log('wcfe', this.searchresults) 
            } 
        })
        this.data.connect()
    }

    disconnectedCallback() {
        console.log('closing')
        this.data.close()
    }


    throttledChanged() {
        const val = this.textInput.value.toLowerCase() //make a copy of it, remove morph boundaries from selected string
        if (this.data.isOpen()) {
            console.log('throttled: ', val, this.throttle);
            const words = val.split(' ')
            const lastword = words[words.length - 1]
            this.data.search(lastword, this.limit)
        }
    }

    preThrottled() {
        const val = this.textInput.value // make a copy of it
        if (val === '') {
            this.searchresults = {results: [], total: 0}
            return
        } else if (val.length > 2) {
            this.throttled()
        }
    }

    onHitClick(item){
        this.textInput.value = item[0].split(" ")[0]
        this.currentWord = item[0].split(" ")[0]
        this.preThrottled()
    }
    copyToClipboard(currentWord) {
        /* Get the text field */
        var dummy = document.createElement("textarea");
        // to avoid breaking orgain page when copying more words
        // cant copy when adding below this code
        // dummy.style.display = 'none'
        document.body.appendChild(dummy);
        //Be careful if you use texarea. setAttribute('value', value), which works with "input" does not work with "textarea". – Eduard
        dummy.value = currentWord;
        dummy.select();
        document.execCommand("copy");
        document.body.removeChild(dummy);  
      } 
    render() {
        return (
            <div class="app">
                <div class="header">
                    {/* <img src={logo} class="logo" alt="logo" /> */}
                    <h3>Plains Cree Word Builder </h3>
                </div>
                <br></br>
                <div class="text-display">
                    <h2 id="word">{this.currentWord}</h2>
                </div>
                <br></br>
                <div>
                        <button class="copyButton" onClick={() => this.copyToClipboard(this.currentWord)}>Copy Word</button> 
                </div>
                <div class="body">
                    <div class="row">
                        <div class="column">
                            <div class="searchbox">
                                <form onSubmit={(e) => this.handleSubmit(e)}>
                                    <input
                                        class="inputbox"
                                        type="text"
                                        ref={(el) => this.textInput = el as HTMLInputElement}
                                        onKeyUp={() => this.preThrottled()}>
                                    </input>
                                    {/* <input type="submit" class= "inputButton" value="Submit" /> */}
                                </form>
                                <div class="results">
                                    {
                                        this.searchresults.results.map((result) => //result here is a tuple(str, bool), where the str is the form, and the bool tells us if its a complete form
                                            <div class="hit" onClick={() => this.onHitClick(result)}>
                                                {
                                                    result[2] //todo: put result[2] here: the prefix
                                                }
                                            <b>{result[1] && (result[3] + " ✔") || (result[3])}</b>
                                            </div>
                                        )
                                    }
                                    {
                                        this.searchresults.total > this.limit ?
                                            <div class="hit">
                                                + {this.searchresults.total - this.limit} more...
                                            </div> :
                                            null
                                    }
                                </div>
                            </div>
                            
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}
