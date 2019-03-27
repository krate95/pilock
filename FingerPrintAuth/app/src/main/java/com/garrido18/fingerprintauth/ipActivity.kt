package com.garrido18.fingerprintauth

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley
import kotlinx.android.synthetic.main.server_ip.*
import org.json.JSONObject
import java.lang.Exception

class ipActivity : AppCompatActivity() {

    val TAG ="com.garrido18.fingerprintauth.ipActivity.IP"
    val TAG2 ="com.garrido18.fingerprintauth.ipActivity.DOOR"
    var ip: String? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.server_ip)

        ipButton.setOnClickListener{

            ip = ipTextInput.text.toString()
            getDoorStatusVolley("$ip/get")
        }
    }

    private fun getDoorStatusVolley(url:String){
        val queue = Volley.newRequestQueue(this)

        val get = StringRequest(Request.Method.GET,url, Response.Listener<String> {
                response ->
            try{
                val intent = Intent(this, MainActivity::class.java)
                intent.putExtra(TAG, ip)
                val json = JSONObject(response)
                var door = json.getBoolean("Open")
                intent.putExtra(TAG2,door)
                startActivity(intent)
            }catch(e: Exception){

            }
        }, Response.ErrorListener {  })

        queue.add(get)
    }
}