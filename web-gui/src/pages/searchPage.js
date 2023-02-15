import React, { useState, useEffect } from 'react';
import { GET } from '../helpers/requests';
import ArticleListElement from '../components/articleListElement';
import { useSearchParams } from "react-router-dom";
import SearchField from '../components/searchField';
import TopicListElement from '../components/topicListElement';

function SearchPage() {
  let [searchParams, setSearchParams] = useSearchParams();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState();
  const [page, setPage] = useState();
  const [pageList, setPageList] = useState([]);

  const HITS_PER_PAGE = 20;
  

  let search = (query, p) => {
    GET(`/search/?q=${query}&count=${HITS_PER_PAGE}&page=${p}`)
      .then(response => setResults(response.data))
  }
  useEffect(() => {
    let p = searchParams.get('page');
    if (p) {
      setPage(parseInt(p));
    } else {
      p = 1
      setPage(p);
    }
    let q = searchParams.get('q');
    if (q) {
      setQuery(q);
      search(q, p);
    };
  }, []);

  useEffect(() => {
    if (!results) return;
    let start = 1;
    let end = 5;
    if (page < (Math.ceil(results.hitCount / HITS_PER_PAGE) - 2)) {
      if (page < 3) {
        if (Math.ceil(results.hitCount / HITS_PER_PAGE) < 5) {
          end = Math.ceil(results.hitCount / HITS_PER_PAGE);
        }
      } else {
        end = page + 2;
        start = page - 2;
      }
    } else {
      end = Math.ceil(results.hitCount / HITS_PER_PAGE);
      if (page < 5) {
        start = 1;
      } else {
        start = end - 5;
      }
    }
    setPageList(Array.from({length: end - start + 1}, (x, i) => i + start))
  }, [results]);

  return (
      <div className="container mx-auto pt-16 px-3 mb-40">
        <div className="w-full max-w-xl">
          <SearchField />
          {results && 
            <div className="mt-3">
              <div className="text-sm text-gray-600">Took: {results.took}s</div>
              {results.suggestion &&
                <div className="text-gray-600">Meintest du: <a href={`/search?q=${results.suggestion}`}><span className="text-slate-800" dangerouslySetInnerHTML={{__html: results.suggestion_html}} /></a></div>
              }
            </div>
          }
        </div>
        <div className="w-full max-w-4xl">
          {results
            ? 
              <div className="mt-10">
                {results.content.map(content => {
                  return (
                    content.type === 'topic'
                      ? <TopicListElement topic={content} />
                      : <ArticleListElement article={content} />
                  )})
                }
                <div className='mt-14'>
                  <a 
                    href={`/search?q=${query}&page=${page - 1}`}
                    disabled={page == 1 ? true : false} 
                    className={`rounded-l-full border px-3 py-2 font-bold ${page == 1 ? "bg-slate-200 text-gray-500 cursor-not-allowed" : "hover:bg-slate-100 cursor-pointer"}`}
                  >Zurück</a>
                  {pageList.map((site_page) => 
                    <a 
                      href={`/search?q=${query}&page=${site_page}`}
                      disabled={page == site_page ? true : false} 
                      className={`border-y border-r px-3 py-2 font-bold ${page == site_page ? "bg-slate-200 text-gray-500 cursor-not-allowed" : "hover:bg-slate-100 cursor-pointer"}`}
                    >{site_page}</a>
                  )}
                  <a 
                    href={`/search?q=${query}&page=${page + 1}`}
                    disabled={page == Math.ceil(results.hitCount / HITS_PER_PAGE) ? true : false} 
                    className={`rounded-r-full border-y border-r px-3 py-2 font-bold ${page == Math.ceil(results.hitCount / HITS_PER_PAGE) ? "bg-slate-200 text-gray-500 cursor-not-allowed" : "hover:bg-slate-100 cursor-pointer"}`}
                  >Weiter</a>
                </div>
              </div>
            :
              <div className="mt-10">
                <div className="pt-3">
                  <div className="text-sm"></div>
                </div>
                {Array.from({length: 20}, (x, i) => i).map(_ => 
                  <div class="animate-pulse my-4">
                    <div class="h-3 mb-2 w-full max-w-sm bg-slate-400 rounded col-span-2"></div>
                    <div class={`h-4 w-full ${["max-w-xs", "max-w-sm", "max-w-md", "max-w-lg"][Math.floor(Math.random() * 4)]} bg-slate-400 rounded col-span-2`}></div>
                  </div>
                )}
              </div>
          }
        </div>
      </div>
  );
}

export default SearchPage;
