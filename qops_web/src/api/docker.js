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
