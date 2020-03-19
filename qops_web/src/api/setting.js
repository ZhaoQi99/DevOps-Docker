import axios from "@/libs/request";

export function getSetting(data) {
  return axios.request({
    url: "/setting/",
    data: data,
    method: "post"
  });
}
