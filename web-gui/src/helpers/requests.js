import axios from 'axios';

let DOMAIN = "http://localhost:8001";

let get_headers = async () => {
  // const user = await refreshToken();
  // if (user)
  //   return { Authorization: 'Bearer ' + user.access };
  return {};

}

export async function GET(path) {
  let headers = await get_headers();
  return axios.get(`${DOMAIN}${path}`, {headers: headers})
}

export async function POST(path, data=null, use_auth=true) {
  let headers = {};
  if (use_auth)
    headers = await get_headers(); 
  return axios.post(`${DOMAIN}${path}`, data, {headers: headers})
}

export async function DELETE(path) {
  let headers = await get_headers();
  return axios.delete(`${DOMAIN}${path}`, {headers: headers})
}