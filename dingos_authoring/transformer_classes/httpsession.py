from .__object_base__ import *


class transformer_class(transformer_object):
    def process(self, properties):
        cybox_http_session = http_session_object.HTTPSession()
        cybox_http_session.http_request_response = [self.__create_cybox_http_request_response(properties)]
        return cybox_http_session
        

    def __create_cybox_http_request_response(self, properties):
        cybox_http_request_response = http_session_object.HTTPRequestResponse()
        #cybox_http_request_response.ordinal_position = 
        cybox_http_request_response.http_client_request = self.__create_cybox_http_client_request(properties)
        #cybox_http_request_response.http_provisional_server_response = self.__create_cybox_http_provisional_server_response(properties)
        #cybox_http_request_response.http_server_response = self.__create_cybox_http_server_response(properties)
        return cybox_http_request_response

    def __create_cybox_http_client_request(self, properties):
        cybox_http_client_request = http_session_object.HTTPClientRequest()

        request_line = http_session_object.HTTPRequestLine()
        request_line.http_method = String(properties['method'])
        request_line.value = String(properties['uri'])
        #request_line.version = 
        cybox_http_client_request.http_request_line = request_line

        request_header = http_session_object.HTTPRequestHeader()
        #request_header.raw_header =
        request_header_fields = http_session_object.HTTPRequestHeaderFields()
        request_header_fields.host = http_session_object.HostField()
        request_header_fields.host.domain_name = self.create_cybox_uri_object(properties['host'])
        request_header_fields.host.port = http_session_object.Port()
        port = properties['port']
        try:
            port = int(port)
        except:
            port = 0
        request_header_fields.host.port.port_value = port
        request_header_fields.user_agent = String(properties['user_agent'])
        #request_header_fields...
        request_header.parsed_header = request_header_fields
        cybox_http_client_request.http_request_header = request_header

        message_body = http_session_object.HTTPMessage()
        #message_body.length =
        #message_body.message_body =
        cybox_http_client_request.http_message_body = message_body

        return cybox_http_client_request
