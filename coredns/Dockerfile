ARG DEBIAN_IMAGE=debian:stable-slim
ARG BASE=gcr.io/distroless/static-debian11:nonroot
FROM --platform=$BUILDPLATFORM ${DEBIAN_IMAGE} AS build
SHELL [ "/bin/sh", "-ec" ]

RUN export DEBCONF_NONINTERACTIVE_SEEN=true \
  DEBIAN_FRONTEND=noninteractive \
  DEBIAN_PRIORITY=critical \
  TERM=linux ; \
  apt-get -qq update ; \
  apt-get -yyqq upgrade ; \
  apt-get -yyqq install ca-certificates libcap2-bin git build-essential curl wget; \
  apt-get clean

RUN wget https://go.dev/dl/go1.23.2.linux-amd64.tar.gz
RUN rm -rf /usr/local/go && tar -C /usr/local -xzf go1.23.2.linux-amd64.tar.gz
ENV PATH="$PATH:/usr/local/go/bin"

RUN git clone https://github.com/coredns/coredns --depth 1

WORKDIR /coredns
COPY plugin.cfg plugin.cfg
RUN go clean -modcache
RUN go get github.com/ldlac/blocker
RUN go generate
RUN GOARCH=amd64 go build -o coredns
RUN setcap cap_net_bind_service=+ep ./coredns

FROM --platform=$BUILDPLATFORM ${DEBIAN_IMAGE}
SHELL [ "/bin/sh", "-ec" ]
COPY --from=build /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=build /coredns/coredns /coredns
WORKDIR /
EXPOSE 53 53/udp
ENTRYPOINT ["/coredns"]

