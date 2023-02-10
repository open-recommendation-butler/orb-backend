import React, { useState, useEffect } from 'react';

function Navbar() {

  return (
    <div className="bg-white absolute w-full">
      <div className="container mx-auto flex justify-between px-3 py-2">
        <div className="font-bold">
          <a href="/">
            <div className="flex items-center">
              <div className="m-0 ml-2">Open Recommendation Butler</div>
            </div>
          </a>
        </div>
        <div>
          <a href="https://github.com/open-recommendation-butler" target="_blank">GitHub</a>
        </div>
      </div>
    </div>
  );
}

export default Navbar;
