import React, { useState, useEffect } from 'react';
import { GET } from '../helpers/requests';
import ArticleListElement from '../components/articleListElement';
import { useSearchParams } from "react-router-dom";

function SearchPage() {
  let [searchParams, setSearchParams] = useSearchParams();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState();

  let search = (query) => {
    GET(`/article/?search=${query}`)
      .then(response => setResults(response.data))
  }
  useEffect(() => {
    let q = searchParams.get('q');
    if (q) {
      setQuery(q);
      search(q);
    };
  }, []);

  let handleSubmit = (event) => {
    if (event) event.preventDefault();
    search(query);
  }
  return (
      <div className="container mx-auto px-3 bg-slate-100 mt-20 mb-20 pb-20">
        <form onSubmit={handleSubmit}>
          <div className="w-full flex">
            <label className="relative block w-full">
              <span className="sr-only">Suche</span>
              <input
                value={query}
                className="placeholder:italic placeholder:text-slate-400 block bg-white w-full border border-slate-300 rounded-md py-3 pl-7 pr-3 shadow-sm focus:outline-none focus:border-slate-600 focus:ring-slate-600 focus:ring-1" 
                placeholder="Nach Artikeln suchen ..." 
                type="text" 
                name="search"
                onChange={(event) => {
                  setQuery(event.target.value);
                  setSearchParams({q: event.target.value});
                }}
              />
            </label>
            <button 
              type="submit"
              className="rounded-md ml-1 text-slate-600 px-4 py-2 font-semibold border border-slate-300 hover:bg-slate-600 hover:text-white hover:border-slate-600 hover:ring-slate-600 hover:ring-1"
            >Suchen</button>
          </div>
        </form>
        {results && 
          <div className="mt-8">
            <h2 className="text-lg font-bold">Neues zu "{results.queryString}"</h2>
            <div className="text-sm">{results.hitCount} Ergebnisse</div>
            {results.suggestion &&
              <div className="">Meintest du: <a href={`/search?q=${results.suggestion}`}><span className="text-slate-800" dangerouslySetInnerHTML={{__html: results.suggestion_html}} /></a></div>
            }
            <div className="mt-5">
              {results.content.map(article => <ArticleListElement article={article} />)}
            </div>
          </div>
        }
      </div>
  );
}

export default SearchPage;
