import axios from "@/libs/request";

export function listHost(params) {
  return axios.request({
    url: "/hosts/",
    params: params,
    method: "get"
  });
}
export function createHost(data) {
  return axios.request({
    url: "/hosts/",
    data: data,
    method: "post"
  });
}
export function updateHost(data) {
  return axios.request({
    url: "/hosts/",
    data: data,
    method: "put"
  });
}
export function deleteHost(data) {
  return axios.request({
    url: "/hosts/",
    data: data,
    method: "delete"
  });
}
