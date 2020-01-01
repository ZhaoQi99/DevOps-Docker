# 系统功能
> *号为非必需

* 登录认证
	* 本地登录(JWT)
	* LDAP认证
	* Google-Authority(QR认证)
* 仪表盘
	* 主机数量
	* 容器状态
	* 应用部署
	* 告警趋势
	* 发布趋势
* 主机管理
	* 主机列表
	* 主机系统资源使用状态(CPU,网络,内存,存储)
	* 主机上运行的容器 -> 容器管理
	* 批量执行命令 *
	* Web Shell *
* 容器管理
	* 容器的创建、停止、重启和删除
	* 容器内执行命令
	* 查看容器日志
	* 容器内资源使用状态
	* 网络、挂载卷的管理 *
* 应用管理
	* 应用 添加、编辑和删除
	* 服务管理(Docker Compose)
	* 服务下容器的管理(多台主机的容器)
	* 负载均衡 *
	* 应用模板 *
* 系统管理
	* 系统设置
	* 用户管理
	* 角色管理
	* 权限管理
	* 审计日志
	* 菜单管理 *
* 镜像仓库管理
	* 支持仓库类型
		* Docker Registry
		* Gitlab Registry
		* VMware Harbor
		* Sonatype Nexus *
		* SUSE Portus *
		* Openstack Glance *
	* 镜像仓库内镜像的管理
* 告警管理
	* 支持告警方式
		* 邮件
		* 对外提供API接口
		* 短信(国内需备案) *
		* 电话外呼 *
		* ~~钉钉~~(不好接入)
		* ~~企业微信~~(可能不好接入)
	* 告警规则配置
	* 监控数据
		* Grafana
		* InfluxDB
* 定时任务管理 * 
* 日志查询
	* Elasticsearch
	* Logstash
* 账号API Key
* 国际化

# 有时间再做的功能
* 容器集群
	* K8S集群
	* Swarm集群 *
* 容器管理平台高可用
* 持续集成
	* Jenkins
	* Gitlab
	* Github *
	* Bitbucket *
* 运维机器人
	* Rocket.Chat
	* Hubot *
	* ~~Slack~~
	* HipChat *

# 现有环境
* Gitlab http://101.200.226.140:8001/
* Jenkins http://101.200.226.140:8002/
* Docker Registry http://101.200.226.140:8003/
* Portainer http://139.9.236.103:9000/
* Rancher http://139.9.236.103:8001/
* PgAdmin http://139.9.236.103:8080/
* Postgres 139.9.236.103:5432
* Redis地址 139.9.236.103:6379