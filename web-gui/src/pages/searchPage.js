import React, { useState, useEffect } from 'react';
import { GET } from '../helpers/requests';
import ArticleListElement from '../components/articleListElement';
import { useSearchParams } from "react-router-dom";
import SearchField from '../components/searchField';

function SearchPage() {
  let [searchParams, setSearchParams] = useSearchParams();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState();

  let search = (query) => {
    GET(`/search/?q=${query}&count=20`)
      .then(response => setResults(response.data))
  }
  useEffect(() => {
    let q = searchParams.get('q');
    if (q) {
      setQuery(q);
      search(q);
    };
  }, []);

  return (
      <div className="container mx-auto pt-16 px-3 mb-20">
        <div className="w-full max-w-xl">
          <SearchField />
          {results && 
            <div className="mt-3">
              <div className="text-sm">{results.hitCount} Ergebnisse</div>
              {results.suggestion &&
                <div className="">Meintest du: <a href={`/search?q=${results.suggestion}`}><span className="text-slate-800" dangerouslySetInnerHTML={{__html: results.suggestion_html}} /></a></div>
              }
            </div>
          }
        </div>
        <div className="w-full max-w-xl">
        {results && 
            <div className="mt-10">
              {results.content.map(article => <ArticleListElement article={article} />)}
            </div>
          }
        </div>
      </div>
  );
}

export default SearchPage;
