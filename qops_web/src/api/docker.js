import axios from "@/libs/request";

export function listContainer(data) {
  return axios.request({
    url: "/docker/containers/",
    data: data,
    method: "post"
  });
}
export function listImage(data) {
  return axios.request({
    url: "/docker/images/",
    data: data,
    method: "post"
  });
}
export function listVolume(data) {
  return axios.request({
    url: "/docker/volumes/",
    data: data,
    method: "post"
  });
}
export function listNetwork(data) {
  return axios.request({
    url: "/docker/networks/",
    data: data,
    method: "post"
  });
}
