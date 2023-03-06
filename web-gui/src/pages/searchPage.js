import React, { useState, useEffect } from 'react';
import { GET } from '../helpers/requests';
import { useSearchParams } from "react-router-dom";
import SearchField from '../components/searchField';
import TopicListElement from '../components/topicListElement';
import SimilarSearchRequests from '../components/similarSearchRequests';

function SearchPage() {
  let [searchParams] = useSearchParams();
  const [query, setQuery] = useState("");
  const [contentType, setContentType] = useState();
  const [results, setResults] = useState();
  const [page, setPage] = useState();
  const [category, setCategory] = useState();
  const [publisher, setPublisher] = useState();
  const [pageList, setPageList] = useState([]);
  const [showFilters, setShowFilters] = useState(false);
  const [showCategories, setShowCategories] = useState(false);
  const [showPublishers, setShowPublishers] = useState(false);

  const categories = [
    'Any category',
    'Politik',
    'Panorama',
    'Sport',
    'Wirtschaft',
    'Kultur',
    'Technik',
    'Reise',
    'Auto',
    'Gesundheit',
    'Wissen'
  ]

   const publishers = ['Any publisher', 'taz, die tageszeitung']

  const HITS_PER_PAGE = 20;
  

  let search = (query, p, contentType, category, publisher) => {
    GET(`/search/?q=${query}&count=${HITS_PER_PAGE}&page=${p}${contentType ? '&content_type=' + contentType : ''}${category ? '&category=' + category : ''}${publisher ? '&publisher=' + publisher : ''}`)
      .then(response => {
        setResults(response.data)
      })
  }
  useEffect(() => {
    let p = searchParams.get('page');
    let contentType = searchParams.get('content_type');
    let category = searchParams.get('category');
    let publisher = searchParams.get('publisher');

    if (category || publisher) setShowFilters(true);
    if (p) {
      setPage(parseInt(p));
    } else {
      p = 1
      setPage(p);
    }
    let q = searchParams.get('q');
    if (q) {
      setQuery(q);
      setContentType(contentType);
      setCategory(category);
      setPublisher(publisher);
      search(q, p, contentType, category, publisher);
    };
  }, [searchParams]);

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
  }, [results, page]);
  console.log('results.content', results)
  return (
      <div className="container mx-auto pt-16 px-3 mb-40">
        <div className="w-full max-w-xl">
          <SearchField />
          <div className='flex ml-4 mr-2 mt-3 gap-2 border-b border-slate-100'>
            <a href={`/search?q=${query}`}>
              <div className={`flex items-center border-slate-400 pr-3 py-1 ${!contentType ? 'border-b-4' : 'hover:border-b-4'}`}>
                <svg className="mr-1" width="12" height="12" viewBox="0 0 477 448" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="184" cy="184" r="157" stroke="#475569" strokeWidth="75"/>
                  <path d="M298 269L463.5 434.5" stroke="#475569" strokeWidth="75"/>
                </svg>
                <div className={`${!contentType ? 'font-bold text-slate-600' : ''}`}>All</div>
              </div>
            </a>
            <a href={`/search?q=${query}&content_type=article${category ? '&category=' + category : ''}${publisher ? '&publisher=' + publisher : ''}`}>
              <div className={`flex items-center border-slate-400 px-2 py-1 ${contentType === 'article' ? 'border-b-4' : 'hover:border-b-4'}`}>
                <svg className="mr-1" width="10" height="20" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <rect x="19" y="19" width="362" height="362" rx="90" stroke="#475569" strokeWidth="80"/>
                  <path d="M74 123H325.5M74 199H325.5M74 276H325.5" stroke="#475569" strokeWidth="55"/>
                </svg>
                <div className={`${contentType === 'article' ? 'font-bold text-slate-600' : ''}`}>Articles</div>
              </div>
            </a>
            <a href={`/search?q=${query}&content_type=podcast${category ? '&category=' + category : ''}${publisher ? '&publisher=' + publisher : ''}`}>
              <div className={`flex items-center border-slate-400 px-2 py-1 ${contentType === 'podcast' ? 'border-b-4' : 'hover:border-b-4'}`}>
              <svg className="mr-1" width="9" height="11" viewBox="0 0 320 396" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="103" y="30" width="117" height="200" rx="100" stroke="#475569" strokeWidth="65"/>
                <path d="M19.013 160C18.3289 212 44.3795 316 154.055 316C263.73 316 301 227.388 301 160" stroke="#475569" strokeWidth="65"/>
                <path d="M159 314V371" stroke="#475569" strokeWidth="65"/>
                <path d="M53 377H261" stroke="#475569" strokeWidth="65"/>
              </svg>
                <div className={`${contentType === 'podcast' ? 'font-bold text-slate-600' : ''}`}>Podcasts</div>
              </div>
            </a>
            <div className='mb-1 ml-auto'>
              <button 
                className={`rounded-xl px-3 py-1 ${showFilters ? 'bg-slate-300 hover:bg-slate-100': 'hover:bg-slate-300'}`} 
                onClick={() => {setShowFilters(!showFilters); setShowCategories(false); setShowPublishers(false)}}
              >Filter</button>
            </div>
          </div>
          {showFilters &&
            <div className='mt-1 text-sm ml-1 flex'>
              <div className='relative'>
                <button 
                  className="rounded-xl px-3 py-1 hover:bg-slate-300 flex items-center" 
                  onClick={() => {setShowCategories(!showCategories); setShowPublishers(false)}}
                >
                  {category ? category : 'Any category'}
                  <svg className={`ml-1 transition-all duration-300 ${showCategories && 'rotate-180'}`} width="9" height="7" viewBox="0 0 172 149" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M86 149L0.263502 0.499984L171.737 0.499999L86 149Z" fill="black"/>
                  </svg>
                </button>
                {showCategories &&
                  <div className='w-52 absolute bottom-0 translate-y-full bg-white border border-slate-200 drop-shadow-2xl rounded-2xl py-4 text-base'>
                    {categories.map((c) => 
                      <a href={`/search?q=${query}${c === 'Any category' ? '' : "&category=" + c}${contentType ? '&content_type=' + contentType : ''}${publisher ? '&publisher=' + publisher : ''}`}>
                        <div className={`flex py-1 px-4 ${(category === c || (c === 'Any category' && !category)) ? 'bg-slate-300' : 'hover:bg-slate-300'}`}>
                          {c}
                        </div>
                      </a>
                    )}
                  </div>            
                }
              </div>
              <div className='relative'>
                <button 
                  className="rounded-xl px-3 py-1 hover:bg-slate-300 flex items-center" 
                  onClick={() => {setShowPublishers(!showPublishers); setShowCategories(false)}}
                >
                  {publisher ? publisher : 'Any publisher'}
                  <svg className={`ml-1 transition-all duration-300 ${showPublishers && 'rotate-180'}`} width="9" height="7" viewBox="0 0 172 149" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M86 149L0.263502 0.499984L171.737 0.499999L86 149Z" fill="black"/>
                  </svg>
                </button>
                {showPublishers &&
                  <div className='w-52 absolute bottom-0 translate-y-full bg-white border border-slate-200 drop-shadow-2xl rounded-2xl py-4'>
                    {publishers.map((p) => 
                      <a href={`/search?q=${query}${p === 'Any publisher' ? '' : "&publisher=" + p}${contentType ? '&content_type=' + contentType : ''}${category ? '&category=' + category : ''}`}>
                        <div className={`flex py-1 px-4 ${publisher === p || (p === 'Any publisher' && !publisher) ? 'bg-slate-300' : 'hover:bg-slate-300'}`}>
                          {p}
                        </div>
                      </a>
                    )}
                  </div>            
                }
              </div>
            </div>
          }
          {results && !showFilters &&
            <div className="mt-2 pb-1 ml-4">
              <div className="text-sm text-gray-600">{results.hitCount} results in {results.took}s</div>
              {results.correction &&
                <div className="text-gray-600">Meintest du:&nbsp;
                  <a href={`/search?q=${results.correction}${contentType ? '&content_type=' + contentType : ''}${category ? '&category=' + category : ''}${publisher ? '&publisher=' + publisher : ''}`}>
                    <span className="text-slate-800" dangerouslySetInnerHTML={{__html: results.correction_html}} />
                  </a>
                </div>
              }
            </div>
          }
        </div>
        <div className="w-full max-w-xl px-4">
          {results
            ? 
              results.hitCount
                ?
                  <div className="mt-10">
                    {results.content.map(content => <TopicListElement topic={content} />)}
                    <SimilarSearchRequests similar_search_requests={results.similar_search_requests} />
                    <div className='mt-14'>
                      <a 
                        href={`/search?q=${query}&page=${page - 1}${contentType ? '&content_type=' + contentType : ''}${category ? '&category=' + category : ''}${publisher ? '&publisher=' + publisher : ''}`}
                        onClick={(e) => page == 1 && e.preventDefault()} 
                        className={`rounded-l-full border px-3 py-2 font-bold ${page == 1 ? "bg-slate-200 text-gray-500 cursor-not-allowed" : "hover:bg-slate-100 cursor-pointer"}`}
                      >Zurück</a>
                      {pageList.map((site_page) => 
                        <a 
                          href={`/search?q=${query}&page=${site_page}${contentType ? '&content_type=' + contentType : ''}${category ? '&category=' + category : ''}${publisher ? '&publisher=' + publisher : ''}`}
                          onClick={(e) => page == site_page && e.preventDefault()} 
                          className={`border-y border-r px-3 py-2 font-bold ${page == site_page ? "bg-slate-200 text-gray-500 cursor-not-allowed" : "hover:bg-slate-100 cursor-pointer"}`}
                        >{site_page}</a>
                      )}
                      <a 
                        href={`/search?q=${query}&page=${page + 1}${contentType ? '&content_type=' + contentType : ''}${category ? '&category=' + category : ''}${publisher ? '&publisher=' + publisher : ''}`}
                        onClick={(e) => page == Math.ceil(results.hitCount / HITS_PER_PAGE) && e.preventDefault()} 
                        className={`rounded-r-full border-y border-r px-3 py-2 font-bold ${page == Math.ceil(results.hitCount / HITS_PER_PAGE) ? "bg-slate-200 text-gray-500 cursor-not-allowed" : "hover:bg-slate-100 cursor-pointer"}`}
                      >Weiter</a>
                    </div>
                  </div>
                :
                  <div className='mt-14'>
                    <p className='text-xl font-bold'>No {contentType ? contentType + 's' : 'results'} found for your query</p>
                    <p className='text-x'>Try another search requests.</p>
                  </div>
            :
              <div className="mt-6">
                <div className="pt-3">
                  <div className="text-sm"></div>
                </div>
                {Array.from({length: 20}, (x, i) => i).map(_ => 
                  <div className="animate-pulse my-4">
                    <div className="h-3 mb-2 w-full max-w-sm bg-slate-400 rounded col-span-2"></div>
                    <div className={`h-4 w-full ${["max-w-xs", "max-w-sm", "max-w-md", "max-w-lg"][Math.floor(Math.random() * 4)]} bg-slate-400 rounded col-span-2`}></div>
                  </div>
                )}
              </div>
          }
        </div>
      </div>
  );
}

export default SearchPage;
