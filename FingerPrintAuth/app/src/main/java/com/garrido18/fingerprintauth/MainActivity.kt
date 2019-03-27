package com.garrido18.fingerprintauth

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.text.Editable
import android.widget.Toast
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley
import com.niravtukadiya.compat.biometric.BiometricCallback
import com.niravtukadiya.compat.biometric.BiometricCompat
import com.niravtukadiya.compat.biometric.BiometricError
import kotlinx.android.synthetic.main.activity_main.*
import org.json.JSONObject
import java.lang.Exception


class MainActivity : AppCompatActivity(), BiometricCallback {

    private var doorStatus: Boolean? = null
    private val IP = intent.getStringExtra("com.garrido18.fingerprintauth.ipActivity.IP")

    override fun onPreConditionsFailed(error: BiometricError) {

        when(error){
            BiometricError.ON_SDK_NOT_SUPPORTED -> Toast.makeText(applicationContext, getString(R.string.biometric_error_sdk_not_supported), Toast.LENGTH_LONG).show()
            BiometricError.ON_BIOMETRIC_AUTH_NOT_SUPPORTED -> Toast.makeText(applicationContext, getString(R.string.biometric_error_hardware_not_supported), Toast.LENGTH_LONG).show()
            BiometricError.ON_BIOMETRIC_AUTH_NOT_AVAILABLE -> Toast.makeText(applicationContext, getString(R.string.biometric_error_fingerprint_not_available), Toast.LENGTH_LONG).show()
            BiometricError.ON_BIOMETRIC_AUTH_PERMISSION_NOT_GRANTED -> Toast.makeText(applicationContext, getString(R.string.biometric_error_permission_not_granted), Toast.LENGTH_LONG).show()
        }

    }

    override fun onCreate(savedInstanceState: Bundle?) {

        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        doorStatus = intent.getBooleanExtra("com.garrido18.fingerprintauth.ipActivity.DOOR",true)

        if (doorStatus == true){
            buttonForm.text = "Cerrar"
        }else{
            buttonForm.text = "Abrir"
        }

        buttonForm.setOnClickListener{
            var pass: String = passForm.text.toString()
            if (pass == "piLock"){
                onAuthenticationSuccessful()
                passForm.setText("")
            }else{
                Toast.makeText(this, "La contraseña es incorrecta", Toast.LENGTH_LONG).show()
            }
        }

        btn_authenticate.setOnClickListener {
            BiometricCompat.BiometricBuilder(this)
                .setTitle(getString(R.string.biometric_title))
                .setLayout(R.layout.custom_view_bottom_sheet)
                .setSubtitle(getString(R.string.biometric_subtitle))
                .setDescription(getString(R.string.biometric_description))
                .setNegativeButtonText(getString(R.string.biometric_negative_button_text))
                .build()
                .authenticate(this)
        }
    }

    override fun onBiometricAuthenticationInternalError(error: String?) {
        Toast.makeText(applicationContext, error, Toast.LENGTH_LONG).show()
    }

    override fun onAuthenticationFailed() {
        //        Toast.makeText(getApplicationContext(), getString(R.string.biometric_failure), Toast.LENGTH_LONG).show();
    }

    override fun onAuthenticationCancelled() {
        Toast.makeText(applicationContext, getString(R.string.biometric_cancelled), Toast.LENGTH_LONG).show()
    }

    override fun onAuthenticationSuccessful() {
        //getDoorStatusVolley("http://krate.ddns.net:5000/get")
        if (doorStatus == true){
            postDoorVolley("$IP/close")
            Toast.makeText(applicationContext,getString(R.string.biometric_success2), Toast.LENGTH_LONG).show()
        }else{
            postDoorVolley("$IP/open")
            Toast.makeText(applicationContext,getString(R.string.biometric_success1), Toast.LENGTH_LONG).show()
        }
    }

    override fun onAuthenticationHelp(helpCode: Int, helpString: CharSequence?) {
        //        Toast.makeText(getApplicationContext(), helpString, Toast.LENGTH_LONG).show();
    }

    override fun onAuthenticationError(errorCode: Int, errString: CharSequence?) {
        //        Toast.makeText(getApplicationContext(), errString, Toast.LENGTH_LONG).show();
    }

    private fun postDoorVolley(url:String){
        val queue = Volley.newRequestQueue(this)
        var jsonobj = JSONObject()
        jsonobj.put("text", "piLock")

        val post = JsonObjectRequest(Request.Method.POST,url,jsonobj,
            Response.Listener {
                    response ->
                try{
                    val json = response
                    doorStatus = json.getBoolean("Open")
                    if (doorStatus == true){
                        buttonForm.text = getString(R.string.buttonFormClose)
                    }else{
                        buttonForm.text = getString(R.string.buttonFormOpen)
                    }
                }catch(e: Exception){}
            }, Response.ErrorListener {})
        queue.add(post)

    }

}
