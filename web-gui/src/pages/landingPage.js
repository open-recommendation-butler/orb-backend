import React, { useState, useEffect } from 'react';
import { GET } from '../helpers/requests';
import { useSearchParams } from "react-router-dom";

function LandingPage() {
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
    <>
      <div className="container mx-auto px-3 h-[90vh] flex">
        <div className='my-auto w-full'>
          <h1 className="text-3xl font-bold text-center text-slate-800 mb-10">Find what feels missing</h1>
          <form onSubmit={handleSubmit}>
            <div className="w-full flex max-w-xl mx-auto">
                <label className="relative block w-full">
                  <span className="sr-only">Suche</span>
                  <svg className="absolute inset-y-2/4 -translate-y-1/2 left-5" width="20" height="20" viewBox="0 0 477 448" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="176" cy="176" r="157" stroke="#475569" strokeWidth="55"/>
                    <path d="M298 269L463.5 434.5" stroke="#475569" strokeWidth="55"/>
                  </svg>
                  <input
                    value={query}
                    className="placeholder:italic placeholder:text-slate-400 block bg-white w-full border border-slate-300 rounded-full py-3 pl-12 pr-3 shadow-sm focus:outline-none focus:border-slate-600 focus:ring-slate-600 focus:ring-1" 
                    type="text" 
                    name="search"
                    autoFocus={true}
                    onChange={(event) => {
                      setQuery(event.target.value);
                      setSearchParams({q: event.target.value});
                    }}
                  />
                </label>
            </div>
          </form>
        </div>
      </div>

      <div className="container mx-auto px-3 mb-20 pb-20">
        <div className="grid md:grid-cols-3 gap-4 mb-14">
          <div className="bg-slate-100 rounded-xl p-6">
            <h4 className='font-bold mb-2'>Results that are worth reading</h4>
            <p>It takes time to find the information you are looking for. This solution is optimized on finding high quality information fast.</p>
          </div>
          <div className="bg-slate-100 rounded-xl p-6">
            <h4 className='font-bold mb-2'>Search without noise</h4>
            <p>Incredibly fast, this tool let's you access information that usually get lost. Orientation instead of redundany.</p>
          </div>
          <div className="bg-slate-100 rounded-xl p-6">
            <h4 className='font-bold mb-2'>Open source state-of-the-art AI tech</h4>
            <p>This solution is a privacy first search. It uses AI tech to improve the results - without depending on your data.</p>
          </div>
        </div>

        <div className="container mx-auto px-3 mb-20 pb-20">
          <h2 className='text-xl font-bold mb-3'>Functions</h2>
        </div>

        <div className="grid md:grid-cols-2 rounded-xl bg-slate-200">
          <div className="bg-slate-300 rounded-xl p-6 relative overflow-hidden">
            <h4 className='z-10 relative text-xl font-bold mb-3'>Explore search options for your media company</h4>
            <a href="https://calendly.com/matthias_meyer/30min" target="_blank">
              <div 
                className="z-10 relative rounded-full bg-slate-800 text-white w-fit px-8 py-2 hover:bg-slate-900"
              >Get a demo</div>
            </a>
            <svg className="z-0 absolute right-0 -bottom-5 pointer-events-none" width="169" height="180" viewBox="0 0 477 448" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="176" cy="176" r="157" stroke="#e2e8f0" strokeWidth="55"/>
              <path d="M298 269L463.5 434.5" stroke="#e2e8f0" strokeWidth="55"/>
            </svg>
          </div>
          <div className="p-6 flex">
            <img className="rounded-xl w-40 mr-4" src={process.env.PUBLIC_URL + '/MatthiasMeyerPortrait.jpg'} />
            <div className="">
              <h4 className=''>Your contact person:</h4>
              <p className='text-xl font-bold mb-3'>Matthias Meyer</p>
              <div className='flex items-center'>
                <a href="mailto:openrecommendationbutler@gmail.com?subject=Request%20for%20Open%20Recommendation%20Butler">
                  <div 
                    className="rounded-full border border-2 border-slate-800 text-slate-800 w-fit px-6 py-2 hover:bg-slate-300"
                  >Mail</div>
                </a>
                <a href="https://www.linkedin.com/in/matth-meyer/" target="_blank" className="text-slate-800 mx-4 underline hover:underline-offset-4">LinkedIn</a>
                <a href="https://twitter.com/Matth_Meyer" target="_blank" className="text-slate-800 underline hover:underline-offset-4">Twitter</a>
              </div>
            </div>
          </div>
        </div>
      </div>

    </>

  );
}

export default LandingPage;
