import axios from "@/libs/request";

export function login(data) {
  return axios.request({
    url: "/account/login/",
    data: data,
    method: "post"
  });
}

export function listPermission(params) {
  return axios.request({
    url: "/account/permissions/",
    method: "get",
    params: params
  });
}

export function deletePermission(data) {
  return axios.request({
    url: "/account/permissions/",
    method: "delete",
    data: data
  });
}
export function updatePermission(data) {
  return axios.request({
    url: "/account/permissions/",
    method: "put",
    data: data
  });
}
export function createPermission(data) {
  return axios.request({
    url: "/account/permissions/",
    method: "POST",
    data: data
  });
}
