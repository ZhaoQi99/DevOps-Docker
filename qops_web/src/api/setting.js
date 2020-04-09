import axios from "@/libs/request";

export function getSetting(data) {
  return axios.request({
    url: "/setting/",
    data: data,
    method: "post"
  });
}
export function listLog(params) {
  return axios.request({
    url: "/logs/",
    params: params,
    method: "get"
  });
}
