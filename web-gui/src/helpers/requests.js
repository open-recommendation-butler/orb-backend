import axios from 'axios';

let DOMAIN = "http://localhost:8000/api";
// let DOMAIN = "https://open-recommendation-butler.tech/api";

export async function GET(path) {
  return axios.get(`${DOMAIN}${path}`)
}

export async function POST(path, data=null) {
  let headers = {};
  return axios.post(`${DOMAIN}${path}`, data)
}

export async function DELETE(path) {
  return axios.delete(`${DOMAIN}${path}`)
}