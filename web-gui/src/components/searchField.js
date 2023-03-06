import React, { useState, useEffect } from 'react';
import { GET } from '../helpers/requests';
import { useSearchParams } from "react-router-dom";

function SearchField({ autoFocus=false }) {
  let [searchParams] = useSearchParams();
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    setQuery(searchParams.get("q"));
  }, [searchParams]);

  let handleChange = (event) => {
    setQuery(event.target.value);
    GET(`/suggestion/?q=${event.target.value}`)
      .then(response => setSuggestions(response.data))
  }

  let handleSubmit = (event) => {
    if (event) event.preventDefault();
    window.location.replace('/search?q=' + query);
  }

  return (
    <form onSubmit={handleSubmit}>
      <label className="relative block w-full">
        <span className="sr-only">Suche</span>
        <svg className="z-20 absolute inset-y-2/4 -translate-y-1/2 left-5" width="20" height="20" viewBox="0 0 477 448" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="184" cy="176" r="157" stroke="#475569" strokeWidth="55"/>
          <path d="M298 269L463.5 434.5" stroke="#475569" strokeWidth="55"/>
        </svg>
        {query &&
          <button 
            type="reset"
            onClick={() => {
              setQuery("");
            }} 
            className="z-20 absolute inset-y-2/4 -translate-y-1/2 right-3 m-0 p-0 w-[35px] h-[35px]"
          >
            <div className="rounded-full w-full h-full flex items-center hover:bg-slate-100">
              <svg className="m-auto" width="20" height="20" viewBox="0 0 429 429" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M14 14L415 415" stroke="#475569" strokeWidth="55"/>
                <path d="M415 14L14 415" stroke="#475569" strokeWidth="55"/>
              </svg>
            </div>
          </button>
        }
        <input
          value={query}
          className="z-10 relative placeholder:italic placeholder:text-slate-400 block bg-white w-full border border-slate-300 rounded-full py-3 px-14 shadow-sm focus:outline-none focus:border-slate-600 focus:ring-slate-600 focus:ring-1" 
          type="text" 
          name="q"
          maxLength={2048}
          autoCapitalize="off" 
          autoComplete="off" 
          autoCorrect="off" 
          autoFocus={autoFocus}
          onChange={handleChange}
        />
      </label>
      {query && query !== searchParams.get("q") &&
        <div className="relative">
          <div className="absolute bg-white border border-slate-300 rounded-2xl py-4 w-full">
            <ul>
              {suggestions.map((suggestion) => 
              <a href={`/search?q=${suggestion}`}>
                <li className="pl-14 pr-4 py-2 hover:bg-slate-100 relative">
                  <svg className="z-20 absolute inset-y-2/4 -translate-y-1/2 left-5" width="20" height="20" viewBox="0 0 477 448" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="184" cy="176" r="157" stroke="#475569" strokeWidth="55"/>
                    <path d="M298 269L463.5 434.5" stroke="#475569" strokeWidth="55"/>
                  </svg>
                  <div>{suggestion}</div>
                </li>
              </a>
              )}
            </ul>
            <div className="flex justify-center">
              <a href={`/search?q=${query}`}>
                <div 
                  className="mr-4 mt-3 rounded-full bg-slate-700 text-white w-fit px-6 py-2 hover:bg-slate-800"
                >
                  Search
                </div>
              </a>
            </div>
          </div>
        </div>
      }
    </form>
  )
}

export default SearchField;
